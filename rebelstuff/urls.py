from django.urls import path

from .admin import site
from .feeds import BookingFeed

urlpatterns = [
    path('', site.urls),
    path('ical/', BookingFeed())
]
