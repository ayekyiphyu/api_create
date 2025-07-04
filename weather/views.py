from rest_framework import generics, permissions
from weather.models import Weather
from weather.serializers import WeatherSerializer

class WeatherCreateView(generics.ListCreateAPIView):
    serializer_class = WeatherSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        return Weather.objects.all()
