from django.shortcuts import render
from .models import Traveler
from .models import Trip
from .models import Review


# def post_list(request):
#     travelers = Traveler.objects.order_by('surname')
#     return render(request, 'test.html', {'travelers': travelers})

def main(request):
    return render(request, 'JointTripApp/index.html')
