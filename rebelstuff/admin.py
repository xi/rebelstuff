from django.contrib import admin

from . import models


class StuffAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount']
    search_fields = ['name']


class BookingItemInline(admin.TabularInline):
    model = models.BookingItem
    autocomplete_fields = ['stuff']


class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'end']
    date_hierarchy = 'start'
    search_fields = ['name']
    inlines = [BookingItemInline]


admin.site.register(models.Stuff, StuffAdmin)
admin.site.register(models.Booking, BookingAdmin)
