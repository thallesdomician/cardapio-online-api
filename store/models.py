import calendar
import datetime

from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from PIL import Image
from io import BytesIO
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import InMemoryUploadedFile

# from .forms import StoreForm
from address.models import Address, AddressAdminInline
from cardapioOnlineApi.base_model import BaseModel
from cardapioOnlineApi.settings import MEDIA_LOGO_THUMBNAIL_SIZE, DAYS_OF_WEEK
from plan.models import Plan
from specialty.models import Specialty
from store.validators import valite_cnpj, validate_logo_size


class Store(BaseModel):
    name = models.CharField(max_length=100, unique=True, )
    logo = models.ImageField(upload_to='store', null=True, blank=True, validators=[validate_logo_size])
    thumbnail = models.ImageField(upload_to='thumbnail', editable=False, blank=True, null=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)
    description = models.TextField(null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True, validators=[valite_cnpj], verbose_name='CNPJ')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)

    def full_plan(self):
        return self.storeplan

    def full_address(self):
        if self.address:
            return self.address.full_address

    full_address.short_description = _('Full Address')

    def _create_thumbnail(self, image_field: ImageFieldFile, thumbnail_image_field: ImageFieldFile, size: tuple):
        if not self.logo:
            return
        image = Image.open(image_field.file.file)
        image.thumbnail(size=size)
        image_file = BytesIO()
        image.save(image_file, image.format)
        thumbnail_image_field.save(
            image_field.name,
            InMemoryUploadedFile(
                image_file,
                None, '',
                image_field.file.content_type,
                image.size,
                image_field.file.charset,
            ),
            save=False
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self._create_thumbnail(image_field=self.logo, thumbnail_image_field=self.thumbnail,
                               size=(MEDIA_LOGO_THUMBNAIL_SIZE, MEDIA_LOGO_THUMBNAIL_SIZE,))
        super(Store, self).save(*args, **kwargs)


class StorePlan(BaseModel):
    store = models.OneToOneField(Store, on_delete=models.CASCADE, primary_key=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    expiration = models.DateTimeField(null=True, blank=True)


class Phone(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    ddd = models.CharField(max_length=2)
    number = models.CharField(max_length=9)
    main = models.BooleanField(default=False)


class OpenDay(BaseModel):
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class OpenTime(BaseModel):
    time = models.TimeField()
    day = models.ForeignKey(OpenDay, on_delete=models.CASCADE)

class StorePlanAdminInline(admin.TabularInline):
    model = StorePlan

class OpenTymeAdminInline(admin.TabularInline):
    model = OpenTime


class OpenDayAdminInline(admin.TabularInline):
    model = OpenDay
    extra = 1


class PhoneAdminInline(admin.TabularInline):
    model = Phone
    extra = 1


class StoreAdmin(admin.ModelAdmin):
    list_filter = ('name', 'active')
    search_fields = ('name',)

    list_display = ('slug', 'name', 'full_address', 'specialty', 'storeplan', 'updated_at', 'active')
    inlines = [
        StorePlanAdminInline,
        PhoneAdminInline,
        AddressAdminInline,
        OpenDayAdminInline
    ]

    # get_full_address.admin_order_field = 'address__full_address'
