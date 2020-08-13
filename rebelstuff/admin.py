from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import models as auth_models
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import models
from .views import ContractView


class Site(admin.AdminSite):
    site_header = 'RebelStuff'
    site_title = 'RebelStuff'
    site_url = '/calendar/'
    index_title = _('Home')


class StuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'available']
    search_fields = ['name']


class BookingItemInline(admin.TabularInline):
    model = models.BookingItem
    autocomplete_fields = ['stuff']
    readonly_fields = ['price']

    def price(self, obj):
        return obj.stuff.price


class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end', 'status', 'price']
    date_hierarchy = 'start'
    search_fields = ['name']
    list_filter = ['status']
    inlines = [BookingItemInline]
    readonly_fields = ['price']

    def get_urls(self):
        return [path(
            '<int:pk>/contract/',
            ContractView.as_view(),
            name='rebelstuff_booking_contract',
        )] + super().get_urls()


site = Site()
site.register(auth_models.User, UserAdmin)
site.register(auth_models.Group)
site.register(models.Stuff, StuffAdmin)
site.register(models.Booking, BookingAdmin)
