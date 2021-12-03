from cart.models import CartOrder
from django.forms import ModelForm
from django import forms

class CartOrderForm(ModelForm):
    
    email = forms.EmailField(required=False)
    class Meta:
        model = CartOrder
        fields = ['email', 'number', 'full_name', 'address', 'delivery']