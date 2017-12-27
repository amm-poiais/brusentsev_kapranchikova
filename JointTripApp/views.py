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
    if request.GET:
        stringdate = request.GET.get('date', '')
        # datetime = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        departure = request.GET.get('departure', '')
        arrival = request.GET.get('arrival', '')
    else:
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


def addtrip(request):
    if request.user.is_authenticated:
        return render(request, 'JointTripApp/addtrip.html')
    else:
        return render(request, 'JointTripApp/signin.html')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'JointTripApp/profile.html')
    else:
        return render(request, 'JointTripApp/signin.html')
