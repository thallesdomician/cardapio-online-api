from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.active = False
        self.save()

    def deleted(self):
        return self.deleted_at is not None

    def save(self, *args, **kwargs):
        if self.active and self.deleted():
            self.deleted_at = None
        super(BaseModel, self).save(*args, **kwargs)

    deleted.short_description = _('Deleted')
    deleted.boolean = True

    class Meta:
        abstract = True
        ordering = ['created_at', 'updated_at']
