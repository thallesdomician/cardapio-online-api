from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

# from .forms import StoreForm
from address.models import Address, AddressAdminInline
from specialty.models import Specialty
from store.validators import valite_cnpj


class Store(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    slug = models.SlugField(max_length=100, editable=False)
    description = models.TextField(null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True, validators=[valite_cnpj], verbose_name='CNPJ')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @property
    def full_address(self):
        return self.address.full_address\

    # get_full_address.short_description = _('Address')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)


class Phone(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    ddd = models.CharField(max_length=2)
    number = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

class PhoneAdminInline(admin.TabularInline):
    model = Phone



class StoreAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name', )
    list_display = ('name', 'full_address', 'specialty', 'active', 'created_at', 'updated_at')
    inlines = [
        PhoneAdminInline,
        AddressAdminInline,
    ]


    # get_full_address.admin_order_field = 'address__full_address'


