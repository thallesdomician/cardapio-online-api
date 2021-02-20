from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


    #TODO: Criar manager para buscar apenas Models com created_at null or blank
    # https://docs.djangoproject.com/en/3.1/topics/db/managers/ 

    def delete(self, using=None, keep_parents=False):
        self.active = False
        self.save()

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['created_at', 'updated_at']
