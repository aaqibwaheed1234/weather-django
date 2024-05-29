from django.urls import path
from .views import  GetWeather
urlpatterns = [
    # path("index/", indexView.as_view(), name="index"),
    path("weather/", GetWeather.as_view(), name="weather"),
]
