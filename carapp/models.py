from django.db import models

class CarType(models.Model):
    name = models.CharField(max_length=50)
    website_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    cartype = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
