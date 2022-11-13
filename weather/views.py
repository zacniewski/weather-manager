import datetime
import matplotlib.pyplot as plt
import re
import requests
from urllib.request import urlopen

from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.templatetags.static import static

from .forms import FavouriteLocationForm
from .models import FavouriteLocation, WeatherData

wak = conf_settings.WEATHER_API_KEY
default_location = conf_settings.DEFAULT_LOCATION
current_weather_api_url = f"https://api.weatherapi.com/v1/current.json"
search_api_url = f"https://api.weatherapi.com/v1/search.json"


def home_page_view(request):
    # checking if user's favourite location exists in database
    fav_loc = (
        FavouriteLocation.objects.filter(owner=request.user)
        .order_by("-created")
        .first()
    )
    if fav_loc:
        chosen_location = fav_loc
    else:
        chosen_location = default_location
    default_weather_api_url = (
        f"{current_weather_api_url}?key={wak}&q={chosen_location}&aqi=no"
    )

    response_current = requests.get(default_weather_api_url).json()

    # saving results to the database
    if response_current:
        saving_single_weather_data(response_current)

    # looking for public IP address
    ip_suggested_locations = set()
    public_ip = get_public_ip_address()
    suggested_ip_locations_api_url = f"{search_api_url}?key={wak}&q={public_ip}"
    response_ip_suggested_location = requests.get(suggested_ip_locations_api_url)
    for item in response_ip_suggested_location.json():
        ip_suggested_locations.add(item["name"])

    return render(
        request,
        "home.html",
        {
            "default_weather_data": response_current,
            "chosen_location": chosen_location,
            "public_ip": public_ip,
            "ip_suggested_locations": ip_suggested_locations,
        },
    )


def current_weather(request):
    query = request.GET.get("weather_query")
    query_weather_api_url = f"{current_weather_api_url}?key={wak}&q={query}&aqi=no"

    # check if weather data are already in the database
    weather_data_from_database = WeatherData.objects.filter(location=query)
    if weather_data_from_database:
        response_current = {"location": {}, "current": {"condition": {}}}
        dict_with_weather_data = list(weather_data_from_database.values())[0]
        print(dict_with_weather_data)
        response_current["location"]["name"] = dict_with_weather_data["location"]
        response_current["location"]["lat"] = dict_with_weather_data["latitude"]
        response_current["location"]["lon"] = dict_with_weather_data["longitude"]
        response_current["location"]["localtime"] = dict_with_weather_data["local_time"]
        response_current["current"]["pressure_mb"] = dict_with_weather_data[
            "pressure_mb"
        ]
        response_current["current"]["wind_kph"] = dict_with_weather_data["wind_kph"]
        response_current["current"]["wind_dir"] = dict_with_weather_data["wind_dir"]
        response_current["location"]["tz_id"] = dict_with_weather_data["timezone"]
        response_current["current"]["cloud"] = dict_with_weather_data["cloudiness"]
        response_current["current"]["humidity"] = dict_with_weather_data["humidity"]
        response_current["current"]["precip_mm"] = dict_with_weather_data[
            "precipitation"
        ]
        response_current["current"]["condition"]["icon"] = dict_with_weather_data[
            "condition_icon"
        ]
        response_current["location"]["country"] = dict_with_weather_data["country"]
        response_current["current"]["temp_c"] = dict_with_weather_data["temperature"]
        response_current["current"]["feelslike_c"] = dict_with_weather_data[
            "feels_like"
        ]
        response_current["current"]["condition"] = dict_with_weather_data["condition"]
    else:
        response_current = requests.get(query_weather_api_url).json()
        # saving results to the database
        if response_current:
            saving_single_weather_data(response_current)

    # looking for neighbourly locations
    neighbour_locations = set()
    search_neighbours_api_url = f"{search_api_url}?key={wak}&q={query}"
    response_search_neighbours = requests.get(search_neighbours_api_url)
    for item in response_search_neighbours.json():
        neighbour_locations.add(item["name"])

    return render(
        request,
        "weather/current-weather.html",
        {
            "current_weather_data": response_current,
            "query": query,
            "neighbour_locations": neighbour_locations,
        },
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
        if response_historical:
            if not all_5_days_data:
                all_5_days_data.update(response_historical.json())
            else:
                all_5_days_data["forecast"]["forecastday"][0]["hour"].extend(
                    response_historical.json()["forecast"]["forecastday"][0]["hour"]
                )

    # plotting historical data
    x = []
    y = []
    for item in all_5_days_data["forecast"]["forecastday"][0]["hour"]:
        x.append(item["time"])
        y.append(item["temp_c"])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(y, color='blue', label='Temperature')
    ax.set_title(f'Data from {today - datetime.timedelta(days=5)} to {today - datetime.timedelta(days=1)}', fontsize=20)
    ax.set_xlabel('Time samples', fontsize=16)
    ax.set_ylabel('Temperature ($^\circ$C)', fontsize=16)
    leg = ax.legend()
    path_to_saved_plot = f"{conf_settings.STATICFILES_DIRS[0]}/plots/{request.user}-chart.png"
    plt.savefig(path_to_saved_plot)

    return render(
        request,
        "weather/historical-weather.html",
        {
            "historical_weather_data": all_5_days_data,
            "query": query,
            "default_location": default_location,
        },
    )


def chart_historical_data(request):
    path_to_saved_plot_in_static = static(f"plots/{request.user}-chart.png")
    return render(request,
                  "weather/chart-with-historical-data.html",
                  {"path_to_saved_plot_in_static": path_to_saved_plot_in_static}
                  )


@login_required
def favourite_location(request):
    if request.method == "POST":
        form = FavouriteLocationForm(request.POST)
        if form.is_valid():
            fav_location = form.save(commit=False)
            fav_location.owner = request.user
            fav_location.save()
            return render(
                request,
                "weather/favourite-location-done.html",
                {"fav_location": fav_location},
            )
    else:
        form = FavouriteLocationForm()
    return render(request, "weather/favourite-location.html", {"fav_loc_form": form})


def saving_single_weather_data(response_data):
    single_weather_data = WeatherData(
        location=response_data["location"]["name"],
        latitude=response_data["location"]["lat"],
        longitude=response_data["location"]["lon"],
        local_time=response_data["location"]["localtime"],
        pressure_mb=response_data["current"]["pressure_mb"],
        wind_kph=response_data["current"]["wind_kph"],
        wind_dir=response_data["current"]["wind_dir"],
        timezone=response_data["location"]["tz_id"],
        cloudiness=response_data["current"]["cloud"],
        humidity=response_data["current"]["humidity"],
        precipitation=response_data["current"]["precip_mm"],
        condition_icon=f"https:{response_data['current']['condition']['icon']}",
        country=response_data["location"]["country"],
        temperature=response_data["current"]["temp_c"],
        feels_like=response_data["current"]["feelslike_c"],
        condition=response_data["current"]["condition"]["text"],
        created=datetime.datetime.now(),
    )
    single_weather_data.save()


def get_public_ip_address():
    data = str(urlopen("http://checkip.dyndns.com/").read())
    return re.compile(r"Address: (\d+\.\d+\.\d+\.\d+)").search(data).group(1)
