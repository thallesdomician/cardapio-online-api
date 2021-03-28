from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

# from .forms import StoreForm
from address.models import Address, AddressAdminInline
from cardapioOnlineApi.settings import DAYS_OF_WEEK
from globals.models.base_model import BaseModel
from plan.models import Plan
from specialty.models import Specialty
from store.validators import valite_cnpj, validate_start_end


class Store(BaseModel):
	name = models.CharField(max_length=100, )
	logo = ImageField(upload_to='store', null=True, blank=True, default='store/default.svg', )
	slug = models.SlugField(max_length=100, unique=True)
	description = models.TextField(null=True, blank=True)
	cnpj = models.CharField(max_length=14, null=True, blank=True, validators=[valite_cnpj], verbose_name='CNPJ')
	specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)

	permissions = (
		('create_store', 'Create Store'),
	)

	def full_plan(self):
		return self.storeplan

	def full_address(self):
		if self.address:
			return self.address.full_address

	full_address.short_description = _('Full Address')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		super(Store, self).save(*args, **kwargs)


class StorePlan(BaseModel):
	store = models.OneToOneField(Store, related_name='plan', on_delete=models.CASCADE, editable=False)
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
	expiration = models.DateTimeField(null=True, blank=True)


class Phone(BaseModel):
	store = models.ForeignKey(Store, related_name='phones', on_delete=models.CASCADE, editable=False)
	ddd = models.CharField(max_length=2)
	number = models.CharField(max_length=9)
	main = models.BooleanField(default=False)


class OpenDay(BaseModel):
	day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
	store = models.ForeignKey(Store, related_name='days', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('day_of_week', 'store')


class OpenTime(BaseModel):
	start = models.TimeField()
	end = models.TimeField()
	day = models.ForeignKey(OpenDay, related_name='times', on_delete=models.CASCADE)

	def clean(self):
		validate_start_end(self.start, self.end)


class StorePlanAdminInline(admin.TabularInline):
	model = StorePlan


class OpenTimeAdminInline(admin.TabularInline):
	model = OpenTime
	extra = 1


class OpenDayAdmin(admin.ModelAdmin):
	list_display = ('day_of_week', 'store')
	inlines = [
		OpenTimeAdminInline,
	]


class OpenDayAdminInline(admin.TabularInline):
	model = OpenDay
	extra = 1


class PhoneAdminInline(admin.TabularInline):
	model = Phone
	extra = 1


class StoreAdmin(admin.ModelAdmin):
	list_filter = ('name', 'active')
	search_fields = ('name',)

	fields = ['name',
	          'slug',
	          'logo',
	          'description',
	          'cnpj',
	          'specialty']
	list_display = ('slug', 'name', 'full_address', 'specialty', 'plan', 'updated_at', 'active')
	inlines = [
		StorePlanAdminInline,
		PhoneAdminInline,
		AddressAdminInline,
		OpenDayAdminInline
	]

# get_full_address.admin_order_field = 'address__full_address'
