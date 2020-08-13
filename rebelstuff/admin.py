from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import models as auth_models
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import models
from .views import ContractView

CALENDAR_ITEM = {
    'name': _('Calendar'),
    'admin_url': '/calendar/',
    'view_only': True,
}


class Site(admin.AdminSite):
    site_header = 'RebelStuff'
    site_title = 'RebelStuff'
    site_url = None
    index_title = _('Home')

    def _build_app_dict(self, request, label=None):
        app_dict = super()._build_app_dict(request, label=label)
        if request.user.has_perm('rebelstuff.view_booking'):
            if 'rebelstuff' in app_dict:
                app_dict['rebelstuff']['models'].append(CALENDAR_ITEM)
            elif app_dict.get('app_label') == 'rebelstuff':
                app_dict['models'].append(CALENDAR_ITEM)
        return app_dict


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
