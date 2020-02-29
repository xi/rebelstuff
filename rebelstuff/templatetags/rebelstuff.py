from django import template
from django.db.models import Case, When, Value, F

register = template.Library()


@register.filter('range')
def _range(n):
    return range(n)


@register.filter
def month_bookingitem_list(stuff, date_list):
    return stuff.bookingitem_set.filter(
        booking__start__lte=date_list[-1],
        booking__end__gte=date_list[0],
    ).annotate(
        start=Case(
            When(booking__start__lt=date_list[0], then=Value(date_list[0])),
            default=F('booking__start'),
        ),
        end=Case(
            When(booking__end__gt=date_list[-1], then=Value(date_list[-1])),
            default=F('booking__end'),
        ),
    )
