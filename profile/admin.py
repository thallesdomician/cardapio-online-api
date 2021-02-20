from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from profile.models import UserAdmin

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
