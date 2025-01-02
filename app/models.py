from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    img = models.ImageField(default="default-profile.png", null=True, blank=True)
    products = models.ManyToManyField('Product', related_name='products', blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,  null=True, unique=True)
    desc = models.TextField(null=True, blank=True)
    img = models.ImageField(default="default.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name