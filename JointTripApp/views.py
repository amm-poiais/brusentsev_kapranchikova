import re

import datetime

from collections import defaultdict
from django.contrib import auth
from django.core.serializers import json
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.core import serializers
from datetime import datetime, timedelta
from JointTripApp.entities import Pair
from .models import Traveler, City
from .models import Trip
from .models import Review
import json


def index(request):
    # обработка нажатия на поездку - присоединение, покинуть, удалить
    if request.POST:
        if request.user.is_authenticated:
            id_trip = request.POST.get('id_trip', '')
            type_request = request.POST.get('type', '')
            if type_request == 'none':
                trip = Trip.objects.get(trip_id=id_trip)
                trip.passengers.add(Traveler.objects.get(user=auth.get_user(request)))
                trip.save()
                return HttpResponse("user")
            elif type_request == 'user':
                trip = Trip.objects.get(trip_id=id_trip)
                trip.passengers.remove(Traveler.objects.get(user=auth.get_user(request)))
                trip.save()
                return HttpResponse("none")
            elif type_request == 'owner':
                trip = Trip.objects.get(trip_id=id_trip)
                trip.delete()
                return HttpResponse("deleted")
    # обработка поиска
    elif request.GET:
        stringdate = request.GET.get('date', '')
        departure = request.GET.get('departure', '')
        arrival = request.GET.get('arrival', '')

        if " - " in stringdate:
            firstdatestr, lastdatestr = stringdate.split(" - ")
            firstdate = datetime.strptime(firstdatestr, '%d.%m.%Y')
            lastdate = datetime.strptime(lastdatestr, '%d.%m.%Y')
            trips = Trip.objects.filter(departure__contains=departure, arrival__contains=arrival,
                                        start_time__range=[firstdate, lastdate])
        elif len(stringdate) != 0:
            firstdate = datetime.strptime(stringdate, '%d.%m.%Y')
            lastdate = firstdate + timedelta(days=1) - timedelta(minutes=1)
            trips = Trip.objects.filter(departure__contains=departure, arrival__contains=arrival,
                                        start_time__range=[firstdate, lastdate])
        else:
            trips = Trip.objects.filter(departure__contains=departure, arrival__contains=arrival)

        triplist = []

        if request.user.is_authenticated:
            for trip in trips:
                if trip.passengers.all().filter(user=auth.get_user(request)).count() != 0:
                    triplist.append(Pair(serializers.serialize('json', [trip]), 'user'))
                elif trip.owner.user == auth.get_user(request):
                    triplist.append(Pair(serializers.serialize('json', [trip]), 'owner'))
                else:
                    triplist.append(Pair(serializers.serialize('json', [trip]), 'none'))
        else:
            for trip in trips:
                triplist.append(Pair(serializers.serialize('json', [trip]), 'none'))

        return JsonResponse(json.dumps(triplist, default=dumper, indent=3), safe=False)
    else:
        if request.user.is_authenticated:
            trips = Trip.objects.all()
            triplist = []
            for trip in trips:
                if trip.passengers.all().filter(user=auth.get_user(request)).count() != 0:
                    triplist.append(Pair(trip, 'user'))
                elif trip.owner.user == auth.get_user(request):
                    triplist.append(Pair(trip, 'owner'))
                else:
                    triplist.append(Pair(trip, 'none'))

            cities = City.objects.all()
            return render(request, 'JointTripApp/index.html', {
                "triplist": triplist,
                "cities": cities
            })
        else:
            trips = Trip.objects.all()
            triplist = []
            for trip in trips:
                triplist.append(Pair(trip, 'none'))

            cities = City.objects.all()
            return render(request, 'JointTripApp/index.html', {
                "triplist": triplist,
                "cities": cities
            })


def signin(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('JointTripApp/signin.html', args)
    else:
        return render_to_response('JointTripApp/signin.html', args)


def signout(request):
    auth.logout(request)
    return redirect('/')


def addtrip(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        departure = request.POST.get('departure', '')
        arrival = request.POST.get('arrival', '')
        seats = request.POST.get('seats', '')
        pets = request.POST.get('pets', '')
        smoke = request.POST.get('smoke', '')
        talk = request.POST.get('talk', '')
        comment = request.POST.get('comment', '')
        price = request.POST.get('price', '')
        trip = Trip(owner=Traveler.objects.get(user=auth.get_user(request)), departure=departure, arrival=arrival,
                    number_of_seats=seats, pets=bool(re.match('on', pets)), smoke=bool(re.match('on', smoke)),
                    talk=bool(re.match('on', talk)), comment=comment, price=price,
                    start_time=datetime.datetime.now())
        trip.save()
        return redirect('/profile.html')
    elif request.user.is_authenticated:
        return render(request, 'JointTripApp/addtrip.html')
    else:
        return render(request, 'JointTripApp/signin.html')


def profile(request):
    if request.user.is_authenticated:
        trips = Trip.objects.filter(owner__user=auth.get_user(request))
        traveler = Traveler.objects.filter(user=auth.get_user(request))[0]
        return render(request, 'JointTripApp/profile.html', {
            "trips": trips,
            "traveler": traveler
            # 'user': auth.get_user(request)
        })
    else:
        return redirect('/signin.html')


def join(request):
    if request.user.is_authenticated:
        Trip.objects.get(trip_id=request.GET.get('id')).passengers.add(Traveler.objects
                                                                       .get(user=auth.get_user(request)))
        return redirect('/')
    else:
        return render(request, 'JointTripApp/signin.html')


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__
