from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.user)


class Product(models.Model):
    title = models.CharField(max_length=256, null=True)
    image = models.URLField(null=True)
    description = models.TextField(null=True)
    price = models.FloatField(null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Order(models.Model):
    SHIPPED = [
        ['Not processed', 'Not processed'],
        ['Out on delivery', 'Out on delivery']
    ]
    name = models.CharField(max_length=256, null=True)
    order_id = models.CharField(max_length=256)
    date = models.DateField(auto_now=True)
    email = models.EmailField(null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    shipped = models.CharField(default="Not processed", max_length=200, choices=SHIPPED)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        #get_latest_by = 'date'
        ordering = ('-date',)