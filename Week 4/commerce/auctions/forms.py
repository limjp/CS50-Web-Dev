from typing import List
from django.db.models.fields import CharField
from django.forms import ModelForm
from .models import Bid, Listing, Comment

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image", "category", "starting_price"]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]