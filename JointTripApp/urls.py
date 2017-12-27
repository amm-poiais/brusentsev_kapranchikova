from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^signin', views.signin, name = 'signin'),
    url('^signout', views.signout, name = 'signout')
]