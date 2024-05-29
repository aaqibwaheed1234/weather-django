from django.db import models

# Create your models here.
class Weather(models.Model):
    city=models.CharField(max_length=32)
    temprature=models.CharField(max_length=32)
    description=models.TextField()
    icon=models.CharField(max_length=255)
    update_date=models.DateTimeField()
    api_response=models.TextField()

    def __str__(self) -> str:
        return self.city