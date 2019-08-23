from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.urls import reverse

from django_ical.views import ICalFeed

from .models import Booking

# not perfect, but still helpful
STATUS_MAP = {
    'waiting': 'TENTATIVE',
    'delivered': 'CONFIRMED',
    'returned': 'CANCELLED',
}

class BookingFeed(ICalFeed):
    def __call__(self, request, *args, **kwargs):
        if request.GET.get('token') != settings.FEED_TOKEN:
            raise PermissionDenied()
        return super().__call__(request, *args, **kwargs)

    def items(self):
        return Booking.objects.all()

    def item_title(self, booking):
        return booking.name

    def item_link(self, booking):
        return reverse('admin:rebelstuff_booking_change', args=[booking.id])

    def item_start_datetime(self, booking):
        return booking.start

    def item_end_datetime(self, booking):
        return booking.end

    def item_status(self, booking):
        return STATUS_MAP[booking.status]

    def item_description(self, booking):
        description = booking.get_status_display() + '\n'

        if booking.contact:
            description += '\n' + booking.contact + '\n'

        for item in booking.bookingitem_set.all():
            item_str = '%s: %i' % (item.stuff.name, item.amount)
            description += '\n' + item_str

        return description
