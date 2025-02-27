from django.urls import path
from weather.views import get_weather, index
from weather.apps import WeatherConfig

app_name = WeatherConfig.name

urlpatterns = [
    path('', index, name='index'),
]