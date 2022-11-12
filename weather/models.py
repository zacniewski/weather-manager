from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class FavouriteLocation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)


class WeatherData(models.Model):
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    local_time = models.CharField(max_length=30)
    pressure_mb = models.CharField(max_length=30)
    wind_kph = models.CharField(max_length=30)
    wind_dir = models.CharField(max_length=30)
    timezone = models.CharField(max_length=30)
    cloudiness = models.CharField(max_length=30)
    humidity = models.CharField(max_length=30)
    precipitation = models.CharField(max_length=30)
    condition = models.CharField(max_length=100)
