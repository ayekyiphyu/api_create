from django.urls import path

from weather.views import WeatherCreateView

urlpatterns = [
    path('weather/', WeatherCreateView.as_view(), name='item-list-create'),
]