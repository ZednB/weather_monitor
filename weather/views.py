import psycopg2
from django.shortcuts import render

from config.settings import WEATHER_API, DATABASES
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


db = DATABASES


def index(request):
    weather = None
    error_mes = None
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather = get_weather(city)
            if weather:
                with psycopg2.connect(
                    dbname='weather_monitor',
                    user='postgres',
                    password='1111'
                ) as conn:
                    with conn.cursor() as cur:
                        cur.execute('''
                        CREATE TABLE IF NOT EXISTS weather (
                        id SERIAL PRIMARY KEY,
                        city VARCHAR,
                        temperature FLOAT
                        );
                        ''')
                        conn.commit()
                        cur.execute(f'''
                        INSERT INTO weather (city, temperature)
                        VALUES ('{weather['city']}',
                        '{weather['current_weather']['temperature']}');
                        ''')
                        conn.commit()
                        cur.close()

            if not weather:
                error_mes = f"Ошибка: нет такого города как {city}"
    else:
        form = WeatherForm
    return render(request, 'weather/index.html', {'form': form, 'weather': weather,
                                                  'error_mes': error_mes})