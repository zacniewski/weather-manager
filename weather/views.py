import datetime
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
        {"current_weather_data": response_current.json(), "query": query},
    )


@login_required
def forecast_weather(request):
    query = request.GET.get("weather_query")
    forecast_weather_api_url = f"https://api.weatherapi.com/v1/forecast.json"
    if query:
        forecast_weather_api_url += f"?key={wak}&q={query}&days=2&aqi=no&alerts=no"
    else:
        forecast_weather_api_url += (
            f"?key={wak}&q={default_location}&days=2&aqi=no&alerts=no"
        )
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
    base_historical_weather_api_url = f"https://api.weatherapi.com/v1/history.json"
    if query:
        place = query
    else:
        place = default_location

    # storage for 5 days JSON data
    all_5_days_data = {}
    today = datetime.date.today()
    for i in range(1, 6):
        previous_day = today - datetime.timedelta(days=i)
        formatted_previous_day = previous_day.strftime("%Y-%m-%d")
        historical_weather_api_url = f"{base_historical_weather_api_url}?key={wak}&q={place}&dt={formatted_previous_day}"
        response_historical = requests.get(historical_weather_api_url)
        if not all_5_days_data:
            all_5_days_data.update(response_historical.json())
        else:
            all_5_days_data["forecast"]["forecastday"][0]["hour"].extend(
                response_historical.json()["forecast"]["forecastday"][0]["hour"]
            )

    return render(
        request,
        "weather/historical-weather.html",
        {
            "historical_weather_data": all_5_days_data,
            "query": query,
            "default_location": default_location,
        },
    )
