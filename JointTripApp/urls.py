from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'/\?*', views.index, name='index'),
    url(r'index*', views.index, name='index'),
    url('^signin', views.signin, name='signin'),
    url('^signout', views.signout, name='signout'),
    url('^profile', views.profile, name='profile'),
    url('^addtrip', views.addtrip, name='addtrip')
]
