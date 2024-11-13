from django.contrib import admin
from .models import CarType, Vehicle, Feature, Buyer, OrderVehicle

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'cartype', 'price', 'instock')
    list_filter = ('cartype', 'features')
    search_fields = ('name',)
    filter_horizontal = ('features',)

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

@admin.register(OrderVehicle)
class OrderVehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'buyer', 'vehicles_ordered')
    list_filter = ('vehicle', 'buyer')
    search_fields = ('vehicle__name', 'buyer__name')
