from django.db import models
from django.utils.timezone import now


# Create your models here.

# Car Make, the __str__ method just returns the name of the car make
class CarMake(models.Model):
    name=models.CharField(primary_key=True,max_length=25)
    description=models.CharField(max_length=150)
    def __str__(self):
        return name


# Car Model, the __str__ method returns the car's year, make, and model
class CarModel(models.Model):
    CAR_TYPES=[
        ("SUV", "SUV"),
        ("Truck", "Truck"),
        ("Sedan", "Sedan"),
        ("Van", "Van"),
        ("Coupe", "Coupe"),
        ("Wagon", "Wagon"),
        ("Convertible", "Convertible"),
        ("Sports Car", "Sports Car"),
        ("Diesel", "Diesel"),
        ("Crossover", "Crossover"),
        ("Luxury Car", "Luxury Car"),
        ("Hybrid/Electric", "Hybrid/Electric")
    ]
    make=models.ManyToManyField(CarMake)
    name=models.CharField(max_length=50)
    dealer_id=models.IntegerField()
    car_type=models.CharField(max_length=20,choices=CAR_TYPES)
    car_year=models.IntegerField()
    def __str__(self):
        return year + " " + make + " " + name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# A plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# A plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealership being reviewed
        self.dealership = dealership
        # Name of reviewer
        self.name = name
        # Did reviewer purchase the car?
        self.purchase = purchase
        # Review text
        self.review = review
        # Date reviewer was in dealership
        self.purchase_date = purchase_date
        # Make of car
        self.car_make = car_make
        # Model of car
        self.car_model = car_model
        # Year car was made
        self.car_year = car_year
        # Sentiment of review
        self.sentiment = sentiment
        # ID number of review
        self.id = id

    def __str__(self):
        return "Review: " + self.review

# <HINT> Create a plain Python class `DealerReview` to hold review data
