from typing import List
from django.db.models.fields import CharField
from django.forms import ModelForm
from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image", "category", "starting_price"]