from django.forms import ModelForm
from .models import Client, Order
from django.contrib.auth.models import User

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['host', 'topic']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['host']
# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']
