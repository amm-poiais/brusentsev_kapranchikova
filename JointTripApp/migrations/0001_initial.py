# Generated by Django 2.0 on 2017-12-27 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Traveler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('trip_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('duration', models.IntegerField(default=0)),
                ('departure', models.CharField(max_length=255)),
                ('arrival', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('price', models.IntegerField(default=0)),
                ('number_of_seats', models.IntegerField(default=0)),
                ('talk', models.BooleanField(default=False)),
                ('smoke', models.BooleanField(default=False)),
                ('pets', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_owner', to='JointTripApp.Traveler')),
                ('passengers', models.ManyToManyField(blank=True, to='JointTripApp.Traveler')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='from_whom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_whom_review', to='JointTripApp.Trip'),
        ),
        migrations.AddField(
            model_name='review',
            name='to_whom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_whom_review', to='JointTripApp.Trip'),
        ),
    ]
