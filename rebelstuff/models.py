import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class Stuff(models.Model):
    name = models.CharField(_('Name'), max_length=64, unique=True)
    description = models.TextField(_('Description'), blank=True)
    amount = models.PositiveIntegerField(_('Amount'))

    def __str__(self):
        return self.name

    def available(self):
        day = datetime.date.today()

        items = BookingItem.objects.filter(
            booking__start__lte=day,
            booking__end__gte=day,
            stuff=self,
        )

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


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(_('Amount'))
