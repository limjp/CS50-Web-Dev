from django.db.models import Max
from django.test import Client, TestCase

from .models import Airport, Flight, Passenger

# Create your tests here.
#Django tests are similar to unittest in the sense that each testing suite has to start with class <Name>TestCase(TestCase)
#The examples here below are testing for models. 
class FlightTestCase(TestCase):

    #To test web applications we need dummy data for our models which we create in setup. 
    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    #Every airport has a departures field which is meant to test how many departures are from that airport. 
    #This basically means given the above data, the amount of departures should be 3. This is to test that departure field working correctly
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    #Departures logic apply for arrivals 
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    #We have deliberately set up valid and invalid flights in setup. So now we are testing the valid ones
    #We are testing the method is_valid_flight within models. 
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    #Testing the invalid ones. Note here we are testing the method is_valid_flight within models
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    #DjangoTest extends beyond unittest functionlaity but also allow you to simulate the sending of requests and responses
    def test_index(self):
        #Client merely means a user browser
        c = Client()
        #This is the request that the client sends towards the endpoint flights
        response = c.get("/flights/")
        print(response)
        #Status Code 200 means okay. Successful response
        #A context is basically a python dictionary that contains variables that the server can pass in when returning a response to a client
        #Here, the endpoint /fights/ has a response that contains 3 flights 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)

    #This is testing another endpoint In general we can test the following (1) That we can obtain a succcessful response as evidenced via the 200 status code (2) That the context
    #returned by the response is correct (3) Contents of the page is correct
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
