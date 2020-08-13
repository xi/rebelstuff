from django.urls import path
from django.conf.urls import url

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
    url(
        r'^stuff-autocomplete/$',
        views.StuffAutoComplete.as_view(model=models.Stuff),
        name='stuff-autocomplete',
    ),
]
