from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class AddressForm(ModelForm):
  class Meta:
    model = Address
    fields = ['phone', 'city', 'street_1', 'street_2', 'postal_code']