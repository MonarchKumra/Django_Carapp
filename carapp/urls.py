from django.urls import path
from . import views

app_name = 'carapp'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('search/', views.search, name='search'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='cardetail'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('orderhere/', views.orderhere, name='orderhere'),
    path('teamdetail/', views.teamdetail, name='teamdetail'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_here, name='login'),
    path('logout/', views.logout_here, name='logout'),
    path('myorders/', views.list_of_orders, name='myorders'),
]
