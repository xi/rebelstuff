from django.contrib import admin
from django.contrib.auth import models as auth_models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class Site(admin.AdminSite):
    site_header = 'RebelStuff'
    site_title = 'RebelStuff'
    index_title = _('Home')


class StuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'available']
    search_fields = ['name']


class BookingItemInline(admin.TabularInline):
    model = models.BookingItem
    autocomplete_fields = ['stuff']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end']
    date_hierarchy = 'start'
    search_fields = ['name']
    inlines = [BookingItemInline]


site = Site()
site.register(auth_models.User, UserAdmin)
site.register(auth_models.Group)
site.register(models.Stuff, StuffAdmin)
site.register(models.Booking, BookingAdmin)
