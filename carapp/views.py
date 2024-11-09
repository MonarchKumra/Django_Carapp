from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.db.models import Q
from .models import CarType, Vehicle

def homepage(request):
    cartype_list = CarType.objects.all().order_by('id')
    return render(request, 'carapp/homepage.html', {'cartype_list': cartype_list})

def aboutus(request):
    return render(request, 'carapp/aboutus.html')

def cardetail(request, cartype_no):
    cartype = get_object_or_404(CarType, id=cartype_no)
    vehicles = Vehicle.objects.filter(cartype=cartype)
    context = {
        'cartype': cartype,
        'vehicles': vehicles,
    }
    return render(request, 'carapp/cardetail.html', context)

class CarDetailView(DetailView):
    model = CarType
    template_name = 'carapp/cardetail.html'
    context_object_name = 'cartype'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.filter(cartype=self.object)
        return context

def search(request):
    query = request.GET.get('q')
    results = CarType.objects.filter(name__icontains=query) if query else None
    return render(request, 'carapp/search.html', {'query': query, 'results': results})

def vehicles(request):
    vehicles_list = Vehicle.objects.all()  # Fetch all vehicles from the database
    return render(request, 'carapp/vehicles.html', {'vehicles': vehicles_list})

def orderhere(request):
    return render(request, 'carapp/orderhere.html', {'message': "You can place your order here."})