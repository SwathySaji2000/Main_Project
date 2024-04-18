from django.contrib import admin

# Register your models here.
from .models import Users, Product

admin.site.register(Users)
admin.site.register(Product)
