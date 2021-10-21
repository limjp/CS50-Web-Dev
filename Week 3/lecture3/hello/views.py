from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #Instead of returning html directly, which would be tedious and not allow easy separation of concerns, we return html templates. To do so , we need to use the render function
    return render(request, "hello\index.html")

def jun_ping(request):
    return HttpResponse("Hello, Jun Ping")

def greet(request, name):
    #render takes a 3rd argument called context. It basically allows you to pass to html arguments that can be called later in the form of a dictionary. So here, we pass in a python
    #dict with key name and value name.capitalize() in greet.html we can call the variable name like this {{ name }} within the variable and it will call name.capitalize()
    return render(request, "hello\greet.html", {
        "name": name.capitalize()
    })