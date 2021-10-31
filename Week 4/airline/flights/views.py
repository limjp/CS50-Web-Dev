from django.shortcuts import render

from .models import Flight

# Create your views here.
#flights.objects.all() -> Basically means getting all rows from flights
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })