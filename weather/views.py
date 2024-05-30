from django.http import JsonResponse
from django.conf import settings
import datetime

import requests
CURRENT_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
CURRENT_WITH_LAT_LON_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric'
API_KEY = settings.WEATHER_API_KEY


def weatherLatLonShow(request):
    lat, lon = request.GET.get('lat'),request.GET.get('lon')
    response = getWeatherData(CURRENT_WITH_LAT_LON_URL.format(lat, lon, API_KEY), FORECAST_URL)
    return JsonResponse(response)


def weatherCityShow(request):
    city = request.GET.get('city')
    response = getWeatherData(CURRENT_URL.format(city, API_KEY), FORECAST_URL)
    return JsonResponse(response)



def getWeatherData(url, forecast_url):
    try:
        response = requests.get(url).json()
        forecast_response = requests.get(forecast_url.format(response['name'], API_KEY)).json()
        res = {}
        res['city']=response['name']
        res['humidity']=response['main']['humidity']
        res['temp']=response['main']['temp']
        res['icon']=response['weather'][0]['icon']
        res['description']=response['weather'][0]['description']
        res['real_feel']=response['main']['feels_like']
        res['wind']=response['wind']['speed']
        res['visibility']=response['visibility']

        today_forecast = []
        week_forecast = []
        for i in forecast_response['list']:
            obj = {}
            obj['temp']=i['main']['temp']
            obj['icon']=i['weather'][0]['icon']
            obj['description']=i['weather'][0]['description']
            obj['time']=i['dt_txt']
            forecast_date = datetime.datetime.strptime(obj['time'], "%Y-%m-%d %H:%M:%S").date().day
            current_date = datetime.datetime.now().day

            if current_date==forecast_date:
                obj['time'] = datetime.datetime.strptime(obj['time'], "%Y-%m-%d %H:%M:%S").strftime("%I:%M%p")
                today_forecast.append(obj)
            else:
                obj['time'] = datetime.datetime.strptime(obj['time'], "%Y-%m-%d %H:%M:%S").strftime("%A")
                week_forecast.append(obj)

        res['today_forecast']=today_forecast
        res['week_forecast']=week_forecast
        return res
    except Exception as e:
        return {"error":True, "message": e}