from django.urls import path
from .views import (
    home_page_view,
    current_weather,
    forecast_weather,
    historical_weather,
    favourite_location,
)


urlpatterns = [
    path("", home_page_view, name="home_page_view"),
    path("current-weather/", current_weather, name="current_weather"),
    path("forecast-weather/", forecast_weather, name="forecast_weather"),
    path("historical-weather/", historical_weather, name="historical_weather"),
    path("favourite-location/", favourite_location, name="favourite_location"),
]
