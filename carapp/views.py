from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import OrderVehicleForm, SignUpForm  
from django.core.exceptions import MultipleObjectsReturned
from .models import CarType, Vehicle, OrderVehicle, Buyer

def homepage(request):
    cartype_list = CarType.objects.all().order_by('id')

    # Count user sessions
    session_count = request.session.get('homepage_count', 0) + 1
    request.session['homepage_count'] = session_count

    # Set cookies
    response = render(request, 'carapp/homepage.html', {'cartype_list': cartype_list, 'session_count': session_count})
    response.set_cookie('homepage_visit', 'You visited the homepage!', max_age=10)  # Cookie lasts for 10 seconds
    return response


def aboutus(request):
    # Count user sessions
    session_count = request.session.get('aboutus_count', 0) + 1
    request.session['aboutus_count'] = session_count

    # Set cookies
    response = render(request, 'carapp/aboutus.html', {'session_count': session_count})
    response.set_cookie('aboutus_visit', 'You visited the About Us page!', max_age=10)  # Cookie lasts for 10 seconds
    return response

# Car Details
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

# Search Functionality
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

# Vehicles List
def vehicles(request):
    vehicles_list = Vehicle.objects.all()
    return render(request, 'carapp/vehicles.html', {'vehicles': vehicles_list})

# Place an Order
@login_required(login_url='carapp:login')
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

# Team Details
def teamdetail(request):
    return render(request, 'carapp/teamdetail.html')

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'carapp/signup.html'
    success_url = reverse_lazy('carapp:login')

def form_valid(self, form):
        response = super().form_valid(form)
        
        # Check if a Buyer already exists with the same email
        existing_buyer = Buyer.objects.filter(email=form.cleaned_data['email']).first()
        
        if not existing_buyer:  # Only create a new Buyer if none exists
            Buyer.objects.create(name=form.cleaned_data['username'], email=form.cleaned_data['email'])
        
        return response

# Login
# def login_here(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('carapp:homepage')
#             else:
#                 return HttpResponse('Your account is disabled.')
#         else:
#             return HttpResponse('Invalid login credentials.')
#     return render(request, 'carapp/login_here.html')

def login_here(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('carapp:homepage')  # Redirect to homepage after successful login
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login credentials.')
    return render(request, 'carapp/login_here.html')

# Logout
@login_required
def logout_here(request):
    logout(request)
    return redirect('carapp:homepage')
    
@login_required
def list_of_orders(request):
    user = request.user
    try:
        # Match buyer using a unique attribute like email or username
        buyer = Buyer.objects.get(email=user.email)  # Assuming email is unique and matches the User model
        orders = OrderVehicle.objects.filter(buyer=buyer)
        if orders.exists():
            return render(request, 'carapp/list_of_orders.html', {'orders': orders})
        else:
            msg = "No orders found for you."
            return render(request, 'carapp/list_of_orders.html', {'msg': msg})
    except Buyer.DoesNotExist:
        msg = "You are not registered as a buyer."
        return render(request, 'carapp/list_of_orders.html', {'msg': msg})