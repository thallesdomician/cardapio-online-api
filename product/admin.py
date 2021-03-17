from django.contrib import admin

# Register your models here.
from product.models import Product, ProductAdmin, Category

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)