import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


class Stuff(models.Model):
    name = models.CharField(_('Name'), max_length=64, unique=True)
    description = models.TextField(_('Description'), blank=True)
    amount = models.PositiveIntegerField(_('Amount'))
    price = models.PositiveIntegerField(_('Price'))

    def __str__(self):
        return self.name

    def available(self, day=None, exclude_item_pk=None):
        if day is None:
            day = datetime.date.today()

        bookings = Booking.objects.filter(
            models.Q(status='delivered') |
            models.Q(
                ~models.Q(status='returned'),
                start__lte=day,
                end__gt=day,
            )
        )

        items = BookingItem.objects.filter(
            booking__in=bookings,
            stuff=self,
        )

        if exclude_item_pk:
            items = items.exclude(pk=exclude_item_pk)

        agg = items.aggregate(models.Sum('amount'))
        booked = agg['amount__sum'] or 0
        return self.amount - booked


class Booking(models.Model):
    name = models.CharField(_('Name'), max_length=64)
    contact = models.TextField(_('Contact'), blank=True)
    start = models.DateField(_('Start'))
    end = models.DateField(_('End'))
    status = models.CharField(_('Status'), choices=[
        ('waiting', _('waiting')),
        ('delivered', _('delivered')),
        ('returned', _('returned')),
    ], max_length=16, default='waiting')

    class Meta:
        ordering = ['-start', '-end', 'status', 'name']

    def __str__(self):
        return self.name

    def clean(self):
        if not self.start or not self.end:
            return

        if self.end <= self.start:
            raise ValidationError({
                'end': _('Must be after start.'),
            })

    @cached_property
    def price(self):
        if not self.id:
            return None

        agg = self.bookingitem_set.aggregate(daily=models.Sum(
            models.F('amount') * models.F('stuff__price')
        ))
        duration = self.end - self.start
        return settings.PRICE_BASE + agg['daily'] * duration.days

    def iter_days(self):
        day = self.start
        while day <= self.end:
            yield day
            day += datetime.timedelta(days=1)


def available_stuff_ids():
    return {
        'id__in': [o.id for o in Stuff.objects.all() if o.available() > 0],
    }


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    stuff = models.ForeignKey(
        Stuff,
        on_delete=models.CASCADE,
        limit_choices_to=available_stuff_ids,
    )
    amount = models.PositiveIntegerField(_('Amount'))

    def clean(self):
        if not self.stuff or not self.amount:
            return

        if not self.booking.start or not self.booking.end:
            return

        available = min(
            self.stuff.available(day, self.pk)
            for day in self.booking.iter_days()
        )
        if self.amount > available:
            raise ValidationError(
                _('Not enough of this stuff. Only %i left.') % available,
            )
