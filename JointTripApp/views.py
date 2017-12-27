from django.contrib import auth
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

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
