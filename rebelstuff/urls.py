from django.urls import path

from .admin import site

urlpatterns = [
    path('', site.urls),
]
