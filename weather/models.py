from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class EventManager(models.Manager):
    """
    "Hide" data that are older than 3 hours.
    In the future these data could be removed with .delete() method for example using Celery.
    """
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(created__gte=timezone.now() - timezone.timedelta(hours=3))
        )


class FavouriteLocation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.location


class WeatherData(models.Model):
    location = models.CharField(max_length=100)
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
    condition_icon = models.URLField(max_length=100)
    country = models.CharField(max_length=30)
    temperature = models.CharField(max_length=10)
    feels_like = models.CharField(max_length=10)
    condition = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now=True)

    objects = EventManager()

    def __str__(self):
        return self.location
