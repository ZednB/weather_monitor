from django.shortcuts import render

from config.settings import WEATHER_API
import requests

from weather.forms import WeatherForm


def get_weather(city):
    request = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API}'
    api = requests.get(request)
    if len(api.json()) > 0:
        api2 = api.json()[0]
        lat, lon = api2['lat'], api2['lon']
        print(lat, lon)
        weather_api = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_api)
        # weather_info = weather_data.json()['current_weather']['temperature']
        # weather_info['city'] = city
        weather_date = weather_data.json()
        weather_date['city'] = city
        print(weather_date)
        return weather_date
    return None


def index(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather = get_weather(city)
    else:
        form = WeatherForm
    return render(request, 'weather/index.html', {'form': form, 'weather': weather})
