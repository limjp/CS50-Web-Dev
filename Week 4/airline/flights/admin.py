from django.contrib import admin

from .models import Flight, Airport, Pasesenger
# Register your models here.
#Django also gives you ability to customize admin page. Below, we are creating settings for how we want to view Flights table in admin page. We are saying flight table to 
#display more information than normal. Read Django documentation to see more of what we can do.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Pasesenger, PassengerAdmin)