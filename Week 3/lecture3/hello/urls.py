from django.urls import path
# from . means from the current directory.
from . import views

urlpatterns = [
    #an empty string here means no additional argument. Means nothing else at the end of the route
    #and argument is what view should be rendered when this url is accessed
    #name is just a string name to represent the path. This makes it easy to reference this path in other parts of the app
    path("", views.index, name="index"),
    path("jun_ping", views.jun_ping, name="jun_ping"),
    #below is an example of how you can parameterize URL arguments i.e. if you want all urls of type string to call the function greet. <str:name> is basically saying
    #any argument of type string in the url we want to assign that url argument to variable name. This is impt as name is later used in greet().
    #However, this runs into the problem of any string url argument in hello will call greet
    path("<str:name>", views.greet, name="greet")
]