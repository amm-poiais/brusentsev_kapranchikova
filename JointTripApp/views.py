import re

import datetime

from collections import defaultdict
from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

from JointTripApp.entities import Pair
from .models import Traveler
from .models import Trip
from .models import Review


def index(request):
    if request.GET:
        stringdate = request.GET.get('date', '')
        departure = request.GET.get('departure', '')
        arrival = request.GET.get('arrival', '')
        trips = Trip.objects.filter(departure__contains=departure, arrival__contains=arrival)
        tripsdict = defaultdict(Trip)
        for trip in trips:
            if trip.objects.filter(passengers__user=auth.get_user(request)).exists():
                tripsdict[trip].append('user')
            elif trip.objects.filter(owner__user=auth.get_user(request)).exists():
                tripsdict[trip].append('owner')
            else:
                tripsdict[trip].append('none')


        return render(request, 'JointTripApp/index.html', {
            "tripsdict": tripsdict

            # 'user': auth.get_user(request)
        })
    else:
        if request.user.is_authenticated:
            trips = Trip.objects.all()
            triplist = []
            for trip in trips:
                if trip.passengers.all().filter(user=auth.get_user(request)).count() != 0:
                    triplist.append(Pair(trip, 'user'))
                elif trip.owner.user==auth.get_user(request):
                    triplist.append(Pair(trip, 'owner'))
                else:
                    triplist.append(Pair(trip, 'none'))

            return render(request, 'JointTripApp/index.html', {
                "triplist": triplist
            })
        else:
            trips = Trip.objects.all()
            triplist = []
            for trip in trips:
                triplist.append(Pair(trip, 'none'))

            return render(request, 'JointTripApp/index.html', {
                "triplist": triplist
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

    elif request.user.is_authenticated:
        return render(request, 'JointTripApp/addtrip.html')
    else:
        return render(request, 'JointTripApp/signin.html')


def profile(request):
    if request.user.is_authenticated:
        trips = Trip.objects.filter(owner__user=auth.get_user(request))
        return render(request, 'JointTripApp/profile.html', {
            "trips": trips
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
