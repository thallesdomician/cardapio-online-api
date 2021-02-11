from django.contrib import admin

from .models import State, StateAdmin
#
#
# admin.site.register(Address)
admin.site.register(State, StateAdmin)
# admin.site.register(City)