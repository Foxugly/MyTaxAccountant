# encoding: utf-8
from django.db import models
from django.conf import settings

class FileUpload(models.Model):
    file = models.FileField(upload_to=settings.UPLOAD_DIR)
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
           return self.file.name
    
    def __str__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(FileUpload, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(FileUpload, self).delete(*args, **kwargs)
