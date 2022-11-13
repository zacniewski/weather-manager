from django import forms

from .models import FavouriteLocation


class FavouriteLocationForm(forms.ModelForm):
    class Meta:
        model = FavouriteLocation
        fields = ("location",)
