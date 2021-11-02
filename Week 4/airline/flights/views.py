from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Pasesenger

# Create your views here.
#flights.objects.all() -> Basically means getting all rows from flights
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    #the below means get the flight from SQL, can also search by pk=flight_id where pk is primary key
    #The only reasons we can access flight.passengers.all() is because the Passenger table has a many to many r/s with flight AND related_name column is filled
    flight = Flight.objects.get(id=flight_id)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        #the below means passenger info will be passed in a form field with name passenger
        passenger = Pasesenger.objects.get(pk=int(request.POST["passenger"]))
        #Below command is telling ORM to add all the necessary information in both table passenger and flights to show that this passenger is now on an additional flight and 
        #that this additional flight has 1 more passenger. At the SQL level this means all the changes to the assoc table and both tables Passenger and Flight
        passenger.flights.add(flight)
        #use reverse cause we don't need to hardcode URL easier to just reverse by their name and if we eventually need to change URL we can just change in urls.py 
        #and not worry about changing every HttpResponseRedirect
        return HttpResponseRedirect(reverse("flight", args=(flight.id)))