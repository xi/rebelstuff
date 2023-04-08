from django.urls import path

from . import views
from .admin import site

urlpatterns = [
    path(
        'calendar/',
        views.CalendarView.as_view(),
        name='calendar',
    ),
    path('', site.urls),
]
