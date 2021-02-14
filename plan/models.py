from django.db import models

# Create your models here.
from cardapioOnlineApi.base_model import BaseModel


class Plan(BaseModel):
    name = models.CharField(max_length=150)
    value = models.DecimalField(max_digits=6, decimal_places=2)
