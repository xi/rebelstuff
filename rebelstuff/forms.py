from dal import autocomplete

from django import forms

from . import models

class BookingItemForm1(forms.ModelForm):
    class Meta:
        model = models.BookingItem
        fields = ('stuff', 'amount')
        widgets = {
            'stuff': autocomplete.Select2(url='stuff-autocomplete')
        }    
