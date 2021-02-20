from django.db import models

# Create your models here.
from globals.models.base_model import BaseModel


class Specialty(BaseModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Specialties'
