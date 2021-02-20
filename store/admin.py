from django.contrib import admin

from .models import Store, StoreAdmin, OpenDay, OpenDayAdmin

admin.site.register(Store, StoreAdmin)
admin.site.register(OpenDay, OpenDayAdmin)

