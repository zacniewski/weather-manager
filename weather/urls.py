from django.urls import path
from .views import home_page_view, current_weather


urlpatterns = [
    path("", home_page_view, name="home"),
    path('current-weather/', current_weather, name="current_weather"),

]
