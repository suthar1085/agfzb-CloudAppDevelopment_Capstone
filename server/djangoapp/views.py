from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# A `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['pwd']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# A `logout_request` view to handle sign out request
def logout_request(request):
    # Log out the user in the request
    logout(request)
    # Redirect the user to the index page
    return redirect('djangoapp:index')

# A `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username=request["username"]
        first_name=request["first-name"]
        last_name=request["last-name"]
        password=request["pwd"]
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password)
            # Login the user and redirect to the index
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://04ec2ae8.us-south.apigw.appdomain.cloud/api/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = 'hthttps://04ec2ae8.us-south.apigw.appdomain.cloud/api/api/dealership'
        dealerships = get_dealers_from_cf(url, **({'id':dealer_id}))
        context['dealer'] = dealerships['id' == dealer_id]
        url = 'https://04ec2ae8.us-south.apigw.appdomain.cloud/api/api/reviews'
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['id' == dealer_id, 'reviews'] = dealer_reviews
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        url = 'https://04ec2ae8.us-south.apigw.appdomain.cloud/api/api/dealership'
        dealerships = get_dealers_from_cf(url, **({'id':dealer_id}))
        context['dealer'] = dealerships[0]
        context['cars'] = CarModel.objects.filter(dealer_id=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        url = 'https://04ec2ae8.us-south.apigw.appdomain.cloud/api/api/reviews'
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        max_id = max([review.id for review in dealer_reviews], default=100)
        new_id = max_id + 1 if max_id >= 100 else max_id + 100

        if 'purchase_check' in request.POST:
            car = CarModel.objects.get(id=request.POST['car'])
            car_make = car.make.name
            car_model = car.name
            car_year = car.year.strftime('%Y')
            json_payload = {
                'review': {
                    'id': new_id,
                    'name': request.user.get_full_name(),
                    'review': request.POST['content'],
                    'purchase': True,
                    'purchase_date': request.POST['purchase_date'],
                    'dealership': dealer_id,
                    'car_make': car_make,
                    'car_model': car_model,
                    'car_year': car_year,
                    'review_time': datetime.utcnow().isoformat()
                }
            }
        else:
            json_payload = {
                'review': {
                    'id': new_id,
                    'name': request.user.get_full_name(),
                    'review': request.POST['content'],
                    'purchase': False,
                    'dealership': dealer_id,
                    'review_time': datetime.utcnow().isoformat()
                }
            }

        add_review_to_cf(url, json_payload)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
