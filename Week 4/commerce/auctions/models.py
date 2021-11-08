from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import ModelState
from django.utils import timezone
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    is_active = models.BooleanField(default=True)
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    current_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.URLField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="listings")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listing_won", blank=True, null=True)
    watchers = models.ManyToManyField(User, blank=True, null=True, related_name="watched_listings")
    
    def __str__(self):
        return f"{self.title, self.current_price}"

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=CASCADE, related_name="bids_placed")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.price}"

class Comment(models.Model):
    comment = models.CharField(max_length=100)
    commented_on = models.ForeignKey(Listing, on_delete=CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=CASCADE, related_name="comments")
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.comment}, {self.author}"