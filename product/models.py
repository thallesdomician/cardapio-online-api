from django.db import models
from django.contrib import admin

# Create your models here.
from globals.models.base_model import BaseModel
from cardapioOnlineApi.settings import MEDIA_THUMBNAIL_SIZE
from globals.image.thumbnail import create_thumbnail
from store.models import Store


class Category(BaseModel):
    name = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='image/thumbnail', editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        create_thumbnail(self, image_field=self.image, thumbnail_image_field=self.thumbnail,
                         size=(MEDIA_THUMBNAIL_SIZE, MEDIA_THUMBNAIL_SIZE,))
        super(ProductImage, self).save(*args, **kwargs)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    verbose_name_plural = 'product_images'
    readonly_fields = ['thumbnail']

# Define a new User admin
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline,)
    list_filter = ('name', 'active', 'category')
    search_fields = ('name',)