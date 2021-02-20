from django.contrib import admin

# Register your models here.
from product.models import Product,ProductAdmin

admin.site.register(Product, ProductAdmin)