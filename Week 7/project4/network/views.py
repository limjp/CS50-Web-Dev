from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

import json

from django.views.decorators.csrf import csrf_exempt
from .models import Post, User
from .forms import PostForm

def index(request):
    all_posts = Post.objects.all().order_by("-date_created")
    paginator = Paginator(all_posts, 10)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    postLikes = {}
    for post in posts:
        postLikes[post] = request.user.does_like(post)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            request.user.create_post(form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/index.html", {
                "form": form,
                "posts": postLikes,
                "page": page
            })
    return render(request, "network/index.html", {
        "post_form": PostForm(),
        "postLikes": postLikes,
        "page": page
    })

@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    follower_count = user.followers.count()
    follow_count = user.following.count()
    all_posts = Post.objects.filter(author = user).all().order_by("-date_created")
    paginator = Paginator(all_posts, 10)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    postLikes = {}
    for post in posts:
        postLikes[post] = request.user.does_like(post)
    
    not_same_user = user != request.user
    currently_follow = request.user.does_follow(user)
    return render(request, "network/profile.html", {
        "follower_count": follower_count,
        "follow_count": follow_count,
        "postLikes": postLikes,
        "page": page,
        "not_same_user": not_same_user,
        "currently_follow": currently_follow,
        "profile": user
    })

@login_required
def following(request):
    all_posts = Post.objects.filter(author__following__follower = request.user).order_by("-date_created")
    paginator = Paginator(all_posts, 10)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    postLikes = {}
    for post in posts:
        postLikes[post] = request.user.does_like(post)
    
    return render(request, "network/following.html", {
        "postLikes": postLikes
    })
    
@csrf_exempt
@login_required
def follow(request):
    if request.method == "POST":
        profileId = json.loads(request.body).get("profileId")
        profile = User.objects.get(id=profileId)
        if request.user.does_follow(profile):
            request.user.unfollow(profile)
            return JsonResponse({f"message": f"Successfully unfollowed {profile}",}, status=201)
        else:
            request.user.follow_user(profile)
            return JsonResponse({"message": f"Successfully followed {profile}"}, status = 201)
    else:
        return JsonResponse({"Error": "Must be a POST request"})

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")