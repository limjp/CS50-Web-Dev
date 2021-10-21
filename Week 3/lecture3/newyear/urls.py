from django.urls import path
# from . means from the current directory.
from . import views

urlpatterns = [
    path("", views.index, name="index")
]