from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(label='Введите название города', max_length=100)
