from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)

# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        #The below means creating a variable form of the same class as NewTaskForm BUT populating its attributes with data in the POST request that the user sent. 
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            #The below is an example of redirecting a user at the end of a page. Note that we never hardcode routes instead, we use the django reverse method to dynamically create
            #the url path to redirect to. In this case, by creating tasks:index. Tasks only works because in urls.py in tasks folder we have included the app_name as tasks
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            #If the form is not valid, we are giving back the form variable because this means that we can include any error messages that Django populates in the form
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })