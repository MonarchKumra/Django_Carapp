from django.db import models

class CarType(models.Model):
    name = models.CharField(max_length=50)
    website_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    instock = models.PositiveIntegerField(default=0)
    cartype = models.ForeignKey(CarType, related_name='vehicles', on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, related_name='vehicles', blank=True)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class OrderVehicle(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='orders', on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, related_name='orders', on_delete=models.CASCADE)
    vehicles_ordered = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.buyer.name} for {self.vehicle.name} (Quantity: {self.vehicles_ordered})"