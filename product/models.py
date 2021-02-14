from django.db import models

# Create your models here.
from cardapioOnlineApi.base_model import BaseModel
from store.models import Store


class Category(BaseModel):
    name = models.CharField(max_length=100)

class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)





