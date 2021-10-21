from django.urls import path
from . import views


#This helps prevent namespace collision by allowing Django to unqiuely identify which urls belong to which apps even if they share the same name
app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
]