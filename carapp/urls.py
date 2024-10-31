from django.urls import path
from . import views

app_name = 'carapp'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('search/', views.search, name='search'),
    # path('car/<int:cartype_no>/', views.cardetail, name='cardetail'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='cardetail'),
]
