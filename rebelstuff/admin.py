from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import models as auth_models
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from dal import autocomplete

from . import models
from .views import ContractView
from .forms import BookingItemForm1


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
    form = BookingItemForm1    
    
    readonly_fields = ['price']

    def price(self, obj):
        return obj.stuff.price

    class Media:
        css = {
            'all': ('autocomplete_light/select2.css', 'disable-add-related.css',)
        }
        js = (
            'autocomplete_light/jquery.init.js',
            'autocomplete_light/jquery.post-setup.js',
            'autocomplete_light/autocomplete.init.js',
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
        )

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
