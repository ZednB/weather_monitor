import requests
from django.test import TestCase
import unittest

from config.settings import WEATHER_API
from weather.views import get_weather


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.city = 'Moscow'
        self.get_weather = get_weather(self.city)

    def test_add(self):
        self.request = f'http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={WEATHER_API}'
        api = requests.get(self.request)
        if len(api.json()) > 0:
            api2 = api.json()[0]
            lat, lon = api2['lat'], api2['lon']
            weather_api = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_data = requests.get(weather_api)
            weather_date = weather_data.json()
            weather_date['city'] = self.city
            self.assertIsNotNone(weather_date)
