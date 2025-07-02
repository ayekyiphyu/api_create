from django.db import models

class Weather(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()                  # Latitude as float
    lng = models.FloatField()                  # Longitude as float
    country = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Weather"
        verbose_name_plural = "Weather"

    def __str__(self):
        return self.name
