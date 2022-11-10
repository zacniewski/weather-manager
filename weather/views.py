import requests

from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

wak = conf_settings.WEATHER_API_KEY
default_location = conf_settings.DEFAULT_LOCATION


def home_page_view(request):
    current_weather_api_url = f"https://api.weatherapi.com/v1/current.json"
    current_weather_api_url += f"?key={wak}&q={default_location}&aqi=no"
    response_current = requests.get(current_weather_api_url)
    return render(
        request,
        "home.html",
        {
            "default_weather_data": response_current.json(),
            "default_location": default_location,
        },
    )


def current_weather(request):
    query = request.GET.get("weather_query")
    current_weather_api_url = f"https://api.weatherapi.com/v1/current.json"
    current_weather_api_url += f"?key={wak}&q={query}&aqi=no"
    response_current = requests.get(current_weather_api_url)
    return render(
        request,
        "weather/current-weather.html",
        {
            "current_weather_data": response_current.json(),
            "query": query
        },
    )


@login_required
def forecast_weather(request):
    query = request.GET.get("weather_query")
    forecast_weather_api_url = f"https://api.weatherapi.com/v1/forecast.json"
    if query:
        forecast_weather_api_url += f"?key={wak}&q={query}&days=2&aqi=no&alerts=no"
    else:
        forecast_weather_api_url += f"?key={wak}&q={default_location}&days=2&aqi=no&alerts=no"
    response_forecast = requests.get(forecast_weather_api_url)
    return render(
        request,
        "weather/forecast-weather.html",
        {
            "forecast_weather_data": response_forecast.json(),
            "query": query,
            "default_location": default_location,
        },
    )


@login_required
def historical_weather(request):
    query = request.GET.get("weather_query")
    historical_weather_api_url = f"http://api.weatherapi.com/v1/history.json"
    # dobrać się do 5 ostatnich dni i je zapisać w JSONie!!!!
    historical_weather_api_url += f"?key={wak}&q={query}&dt=2022-11-06"
    response_historical = requests.get(historical_weather_api_url)
    return render(
        request,
        "weather/historical-weather.html",
        {"forecast_weather": response_historical.json(), "query": query},
    )
