from django.urls import path
from . import views

urlpatterns = [
    path('current', views.weatherLatLonShow),
    path('city', views.weatherCityShow),
]
