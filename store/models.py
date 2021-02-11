from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

# from .forms import StoreForm
from address.models import Address, AddressAdminInline
from specialty.models import Specialty
from store.validators import valite_cnpj


class Store(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, editable=False)
    description = models.TextField(null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True, validators=[valite_cnpj], verbose_name='CNPJ')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)


class Phone(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    ddd = models.CharField(max_length=2)
    number = models.CharField(max_length=9)

class PhoneAdminInline(admin.TabularInline):
    model = Phone



class StoreAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name', )
    list_display = ('name', 'address', 'specialty','active')
    inlines = [
        PhoneAdminInline,
        AddressAdminInline,
    ]


