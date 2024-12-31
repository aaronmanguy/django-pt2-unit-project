from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import Group
# from django.contrib import messages
# from .decorators import *
from .models import *
# from .forms import *

# Create your views here.
def home(request):
    context = {}
    return render(request, 'nav.html', context)