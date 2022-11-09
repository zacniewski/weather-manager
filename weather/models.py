from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class FavouriteLocation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length = 100)


class WeatherData(models.Model):
    pass
