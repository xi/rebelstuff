import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Stuff(models.Model):
    name = models.CharField(_('Name'), max_length=64, unique=True)
    description = models.TextField(_('Description'), blank=True)
    amount = models.PositiveIntegerField(_('Amount'))

    def __str__(self):
        return self.name

    def available(self, day=None, exclude_item_pk=None):
        if day is None:
            day = datetime.date.today()

        items = BookingItem.objects.filter(
            booking__start__lte=day,
            booking__end__gte=day,
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

    class Meta:
        ordering = ['-start', '-end', 'name']

    def __str__(self):
        return self.name

    def clean(self):
        if not self.start or not self.end:
            return

        if self.end < self.start:
            raise ValidationError({
                'end': _('Cannot be before start.'),
            })

    def iter_days(self):
        day = self.start
        while day <= self.end:
            yield day
            day += datetime.timedelta(days=1)


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
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
