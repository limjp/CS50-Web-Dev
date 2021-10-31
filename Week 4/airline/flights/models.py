from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city}, ({self.code})"

class Flight(models.Model):
    #Below is how you declare a foreign key. When declaring foreign keys, there are additional arguments you can pass in to control how your model works. on_delete
    #controls what should happen to this model when the foreign key it is referencing is deleted in another table. models.CASCADE here means delete all rows with that foreign
    #key if the foreign key in the other table is deleted. I.E. Flights now have a foreign key referencing a specific row in Airport. If that row in Airport is deleted, 
    #then delete all the rows in Flights that contain reference to that row in Airport.
    #related_name means a way to access the r/s between models in reverse order. Means from a flight, we can access flight.origin and we get airports. But if we have an 
    #airport, how do we get all the flights that have that airport as an origin. If you pass in related_names then Django will set up that r/s
    #Note: Why does foreign key specify table name instead of specific ID? This is because ORM helps create the ID column for us without explicitly specifying it in py class
    #Hence, when we reference the entire table in foreign key, we are actually referencing the IDs in that table as foreign key. Moreover, ID is always set as primary key.
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.origin}, {self.destination}"