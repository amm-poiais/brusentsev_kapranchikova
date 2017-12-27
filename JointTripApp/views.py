from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response, redirect

from .models import Traveler
from .models import Trip
from .models import Review


# def travelers_list(request):
#     travelers = Traveler.objects.order_by('surname')
#     return render(request, 'test.html', {'travelers': travelers})


def index(request):
    trips = Trip.objects.all()
    return render(request, 'JointTripApp/index.html', {
        "trips": trips
        # 'user': auth.get_user(request)
    })


def signin(request):
    return render(request, 'JointTripApp/signin.html')

def addtrip(request):
    return render(request, 'JointTripApp/addtrip.html')

def profile(request):
    return render(request, 'JointTripApp/profile.html')