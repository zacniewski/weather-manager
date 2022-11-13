from django.contrib import admin
from .models import FavouriteLocation, WeatherData


@admin.register(FavouriteLocation)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in FavouriteLocation._meta.fields if field.name != "id"
    ]


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in WeatherData._meta.fields if field.name != "id"
    ]
