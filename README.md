# Weather Manager by Artur :smiley:
Web application for managing weather data from WeatherAPI


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