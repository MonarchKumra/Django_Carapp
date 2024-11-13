from django import forms
from .models import OrderVehicle

class OrderVehicleForm(forms.ModelForm):
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'vehicles_ordered']
        labels = {
            'vehicles_ordered': 'Vehicles Ordered',
        }
        widgets = {
            'buyer': forms.Select(),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Email ID")
    subject = forms.CharField(max_length=150, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")
