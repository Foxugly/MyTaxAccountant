# encoding: utf-8
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.db import models
from django.conf import settings
import os


class FileUpload(models.Model):
    file = models.FileField(upload_to=settings.UPLOAD_DIR)
    slug = models.SlugField(max_length=255, blank=True)

    def __str__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def get_relative_path(self):
        return os.path.join(settings.UPLOAD_DIR, self.file.path)

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(FileUpload, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(FileUpload, self).delete(*args, **kwargs)
