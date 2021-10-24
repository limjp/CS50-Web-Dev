from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry, name="get_entry"),
    path("search/", views.search, name="search"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.random, name="random")
]
