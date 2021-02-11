from django.contrib import admin

from .models import Store, StoreAdmin

admin.site.register(Store, StoreAdmin)

