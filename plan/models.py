from django.db import models

# Create your models here.
from globals.models.base_model import BaseModel


class Plan(BaseModel):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
