from django import forms

from dal import autocomplete

from . import models


class BookingItemForm(forms.ModelForm):
    class Meta:
        model = models.BookingItem
        fields = ['stuff', 'amount']
        widgets = {
            'stuff': autocomplete.Select2(url='stuff-autocomplete')
        }
