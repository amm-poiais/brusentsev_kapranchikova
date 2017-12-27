from django.shortcuts import render
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

