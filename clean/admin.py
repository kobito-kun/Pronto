from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(OrderItems)
