from django.db import models
from django.contrib import admin

# Create your models here.
from cardapioOnlineApi.base_model import BaseModel


class Specialty(BaseModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Specialties'

class AdminSpecialty(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'deleted')