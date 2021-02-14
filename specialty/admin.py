from django.contrib import admin

from specialty.models import Specialty, AdminSpecialty

admin.site.register(Specialty, AdminSpecialty)