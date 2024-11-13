from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.db.models import Q
from .forms import OrderVehicleForm
from .models import CarType, Vehicle, OrderVehicle

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
    vehicles = Vehicle.objects.all()
    selected_vehicle = None
    price = None

    if request.method == 'POST':
        selected_vehicle_id = request.POST.get('vehicle')
        selected_vehicle = Vehicle.objects.get(id=selected_vehicle_id)
        price = selected_vehicle.price

    return render(request, 'carapp/search.html', {
        'query': query,
        'vehicles': vehicles,
        'selected_vehicle': selected_vehicle,
        'price': price
    })

def vehicles(request):
    vehicles_list = Vehicle.objects.all() 
    return render(request, 'carapp/vehicles.html', {'vehicles': vehicles_list})

def orderhere(request):
    msg = ''
    form = OrderVehicleForm(request.POST or None)
    vehiclelist = Vehicle.objects.all()

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        if order.vehicles_ordered <= order.vehicle.instock:
            order.vehicle.instock -= order.vehicles_ordered 
            order.vehicle.save()
            order.save()
            msg = 'Your vehicle has been ordered successfully.'
        else:
            msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'carapp/nosuccess_order.html', {'msg': msg})

    return render(request, 'carapp/orderhere.html', {'form': form, 'msg': msg, 'vehiclelist': vehiclelist})

def teamdetail(request):
    return render(request, 'carapp/teamdetail.html')