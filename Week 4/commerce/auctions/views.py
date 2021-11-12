from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    all_listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": all_listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            new_listing = Listing(
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                image = form.cleaned_data["image"], 
                category = form.cleaned_data["category"],
                starting_price = form.cleaned_data["starting_price"],
                creator = user
            )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/make_listing.html", {
                "form": form
            })
    return render(request, "auctions/make_listing.html", {
        "listingForm": ListingForm()
    })

def listing(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if "submit_bid" in request.POST and form.is_valid():
            listing = Listing.objects.get(id=listing_id)
            new_bid = Bid(
                price = form.cleaned_data["price"],
                auction = listing,
                bidder = request.user)
            new_bid.save()
            return HttpResponseRedirect(reverse("index"))
        elif "add_watchlist" in request.POST:
            listing = Listing.objects.get(listing_id)
            watchlist_item = Listing.objects.create(watchers=request.user.id)
            listing.watchers.add(watchlist_item)
            return HttpResponseRedirect(reverse("index"))
        elif "close_auction" in request.POST:
            listing = Listing.objects.get(listing_id)
            listing.is_active = False
            listing.save()
        elif not(form.is_valid()):
            return render(request, "auctions/listing.html", {
                "form": form
            })
    listing = Listing.objects.get(id=listing_id)
    all_comments = listing.comments.all()
    is_user_logged_in = request.user.is_authenticated
    is_creator = request.user == listing.creator
    return render(request, "auctions/listing.html", {
        "bid_form": BidForm(),
        "user_id": request.user.id,
        "comments": all_comments,
        "listing": listing,
        "is_user_logged_in": is_user_logged_in,
        "is_creator": is_creator,
        "comment_form": CommentForm()
    })

def create_comment(request, listing_id):
    pass