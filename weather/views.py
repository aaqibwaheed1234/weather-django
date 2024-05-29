from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.conf import settings
from django.http import JsonResponse
from .models import Weather
from datetime import datetime
from collections import defaultdict
# class indexView(LoginRequiredMixin, TemplateView):
#     template_name = "index.html"

# class GetWeather(View):
    # def get(self, request, *args, **kwargs):
    #     city = request.GET.get('city', 'Lahore')
    #     URL = f"http://api.weatherapi.com/v1/current.json?key={settings.WA_APIKEY}&q={city}"
    #     # URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=f085c0dca02bd280d618be48326edbec'
    #     PARMS={'units', 'metric'}
        
    #     print(URL)

    #     try:
    #         res = requests.get(URL)
    #         res.raise_for_status()
    #         res_json = res.json()
    #         print(res_json)

    #         if 'location' in res_json and 'current' in res_json:
    #             weather_data = {
    #                 "city": res_json["location"]["name"],
    #                 "description": res_json["current"]["condition"]["text"],
    #                 "icon": res_json["current"]["condition"]["icon"],
    #                 "temperature": res_json["current"]["temp_c"],
    #                 "updated_date": res_json["current"]["last_updated"],
    #                 "api_response": res.text
    #             }

    #             # Optionally, save data to the database
    #             Weather.objects.create(
    #                 city=weather_data["city"],
    #                 temperature=weather_data["temperature"],
    #                 description=weather_data["description"],
    #                 icon=weather_data["icon"],
    #                 update_date=weather_data["updated_date"],
    #                 api_response=weather_data["api_response"]
    #             )

    #             return JsonResponse(weather_data)
    #         else:
    #             return JsonResponse({'error': 'Invalid response from the Weather API'}, status=400)

    #     except requests.exceptions.RequestException as e:
    #         return JsonResponse({'error': str(e)}, status=400)

class GetWeather(View):
    def get(self, request):
        return render(request, "index.html")
    def post(self, request):
        city = request.POST.get('city')
        weather_data = {}
        _response = {}
        if city:
            city = str(city).strip().lower()
            CURRENT_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.WA_APIKEY}&units=metric"
            FORECAST_URL = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings.WA_APIKEY}&units=metric'

            try:
                current_response = requests.get(CURRENT_URL).json()
                forecast_response = requests.get(FORECAST_URL).json()
                forecast=[]
                for i in forecast_response['list']:
                    day_name = datetime.strptime(i['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime('%A')
                    obj = {
                        "icon":i['weather'][0]['icon'],
                        "temp":i['main']['temp'],
                        "description":i['weather'][0]['description'],
                        "day":day_name,
                    }
                    forecast.extend(obj)

                _response = {
                    "city":current_response['name'],
                    "country":current_response['sys']['country'],
                    "humidity":current_response['main']['humidity'],
                    "wind":current_response['wind']['speed'],
                    "temp":current_response['main']['temp'],
                    "icon":current_response['weather'][0]['icon'],
                    "description":current_response['weather'][0]['description'],
                    "forecast": forecast
                }
                print(_response)

            except requests.exceptions.RequestException as e:
                _response = {'error': str(e)}

        return render(request, 'index.html', {'weather_data': _response})