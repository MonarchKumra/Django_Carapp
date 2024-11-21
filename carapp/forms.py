from django import forms
from .models import OrderVehicle, Buyer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add the email field to the form

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()  # Save the user object first
            
            # Create the corresponding Buyer record for the user
            Buyer.objects.create(name=user.username, email=self.cleaned_data['email'])  # Save email to Buyer
        return user
