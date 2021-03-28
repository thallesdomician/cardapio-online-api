from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from globals.models.base_model import BaseModel


class State(models.Model):
    name = models.CharField(max_length=25)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return '{} - {}'.format(self.name, self.uf)

    class Meta:
        ordering = ['name']


class City(models.Model):
    name = models.CharField(max_length=40)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='city',)

    def __str__(self):
        return '{}/{}'.format(self.name, self.state.uf)

    class Meta:
        verbose_name_plural = _('cities')
        ordering = ['name']


class Address(BaseModel):
    store = models.OneToOneField('store.Store', on_delete=models.CASCADE, related_name='address', editable=False)
    place = models.CharField(max_length=200)
    number = models.CharField(max_length=15)
    complement = models.CharField(max_length=15, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    cep = models.CharField(max_length=8, null=True, blank=True)

    @property
    def full_address(self):
        return '{place}, {number},{complement}{district}{city}/{uf}{cep}'.format(
            place=self.place,
            number=self.number,
            complement='{}, '.format(self.complement) if self.complement else ' ',
            district='{}, '.format(self.complement) if self.district else ' ',
            city=self.city.name,
            uf=self.city.state.uf,
            cep=' - %s%s%s%s%s-%s%s%s' % tuple(self.cep) if self.cep else '')

    def __str__(self):
        return self.full_address


class AddressAdminInline(admin.StackedInline):
    model = Address


class CityAdminInline(admin.TabularInline):
    model = City


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'uf')
    inlines = [
        CityAdminInline,
    ]
