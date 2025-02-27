import requests
from django.test import TestCase
import unittest

from config.settings import WEATHER_API
from weather.views import get_weather


class TestWeather(TestCase):
    def setUp(self):
        self.city = "Moscow"

    def test_get_weather(self):
        weather = get_weather(self.city)
        self.assertIsNotNone(weather)
        self.assertIn("city", weather)
        self.assertIn("current_weather", weather)

    def test_get_weather_invalid_city(self):
        weather = get_weather("FakeCity")
        self.assertIsNone(weather)
