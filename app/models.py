from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.TextField()
    desc = models.TextField(null=True, blank=True)
    img = models.ImageField(default="default.png", null=True, blank=True)

    def __str__(self):
        return self.name