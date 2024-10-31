from django.contrib import admin
from .models import CarType, Vehicle

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'cartype')
    list_filter = ('cartype',)
