from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateProduct(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'
#         exclude = ['user', 'posts']
    