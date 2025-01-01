from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('', home, name='home'),
    path('/create-product', createProduct, name='create-product'),
    path('admin/', admin.site.urls),
]
