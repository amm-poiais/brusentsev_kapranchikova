from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# путешественник - водитель/пассажир
class Traveler(models.Model):
    # user_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return 'Username: %s; Name: %s; Surname: %s; email: %s' % (
            self.user.username, self.name, self.surname, self.email)


# поездка
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)

    owner = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='trip_owner')

    start_time = models.DateTimeField()
    duration = models.IntegerField(default=0)
    departure = models.CharField(max_length=255)
    arrival = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    number_of_seats = models.IntegerField(default=0)

    talk = models.BooleanField(default=False)
    smoke = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)

    passengers = models.ManyToManyField('Traveler', blank=True)


# отзыв
class Review(models.Model):
    from_whom = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='from_whom_review')
    to_whom = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='to_whom_review')
    mark = models.IntegerField(default=0)
    comment = models.CharField(max_length=255)


class City(models.Model):
    name = models.CharField(max_length=255)
