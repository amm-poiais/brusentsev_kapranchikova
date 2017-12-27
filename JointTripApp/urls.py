from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.travelers_list, name='post_list'),
]