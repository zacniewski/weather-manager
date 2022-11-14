# Weather Manager by Artur :smiley:
Web application for managing weather data from WeatherAPI

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/zacniewski/weather-manager.git
$ cd weather-manager

$ # Virtualenv modules installation (Unix based systems)
$ virtualenv my_env (or python -m venv my_env)
$ source my_env/bin/activate

# Virtualenv modules installation (Windows system)
python -m venv <venv-name>
# To activate
#C:\Users\..\<venv-name>
.\Scripts\activate.bat

$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate

$ # Install modules - SQLite Storage
$ pip install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Create app superuser to get to the admin panel
$ python manage.py createsuperuser
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>

$ # Access the web app in browser: http://127.0.0.1:8000/
```

> Note: To get more features (see information below), please access the registration page and create a user
> You can use username or an email
<br />

## Features
1. For non-logged users
  - getting information about the current weather in every place in the world,  
  - suggesting the place of your location (based on your public IP address),  
  - when searching for the Polish locations, please use "Zielona Gora" instead of "Zielona Góra" or "Chelmno" instead of "Chełmno",

2. For registered users
  - all the above,  
  - getting suggestions about the nearby places (based on searched location),  
  - forecast weather for the given location (2 days),  
  - historical weather for the given location (5 past days) + chart of the temperature,  
  - possibility of saving 'favourite' places, these places would be suggested during next search.  


### Example of a response from the [Weather API](https://www.weatherapi.com/api-explorer.aspx)
```json
{
  "location": {
    "name": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom",
    "lat": 51.52,
    "lon": -0.11,
    "tz_id": "Europe/London",
    "localtime_epoch": 1667764612,
    "localtime": "2022-11-06 19:56"
  },
  "current": {
    "last_updated_epoch": 1667763900,
    "last_updated": "2022-11-06 19:45",
    "temp_c": 12.0,
    "temp_f": 53.6,
    "is_day": 0,
    "condition": {
      "text": "Clear",
      "icon": "//cdn.weatherapi.com/weather/64x64/night/113.png",
      "code": 1000
    },
    "wind_mph": 11.9,
    "wind_kph": 19.1,
    "wind_degree": 230,
    "wind_dir": "SW",
    "pressure_mb": 1002.0,
    "pressure_in": 29.59,
    "precip_mm": 0.0,
    "precip_in": 0.0,
    "humidity": 82,
    "cloud": 0,
    "feelslike_c": 9.7,
    "feelslike_f": 49.4,
    "vis_km": 10.0,
    "vis_miles": 6.0,
    "uv": 1.0,
    "gust_mph": 17.9,
    "gust_kph": 28.8,
    "air_quality": {
      "co": 188.60000610351562,
      "no2": 15.399999618530273,
      "o3": 58.70000076293945,
      "so2": 5.199999809265137,
      "pm2_5": 3.200000047683716,
      "pm10": 3.9000000953674316,
      "us-epa-index": 1,
      "gb-defra-index": 1
    }
  }
}
```