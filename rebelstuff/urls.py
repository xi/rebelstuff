from django.urls import path

from . import views
from .admin import site

urlpatterns = [
    path('', site.urls),
    path(
        'calendar/<int:year>/<int:month>/',
        views.CalendarView.as_view(),
        name='calendar',
    ),
]
