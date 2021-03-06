from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("comment/<int:listing_id>", views.create_comment, name="create_comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category")
]
