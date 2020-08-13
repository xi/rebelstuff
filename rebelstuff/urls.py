from django.urls import path

from . import views
from . import models
from .admin import site

urlpatterns = [
    path('', site.urls),
    path(
        'calendar/',
        views.CalendarView.as_view(),
        name='calendar',
    ),
    path(
        'stuff-autocomplete/',
        views.StuffAutoComplete.as_view(),
        name='stuff-autocomplete',
    ),
]
