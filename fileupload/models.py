# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.db import models
from django.conf import settings


class FileUpload(models.Model):
    file = models.FileField(upload_to=settings.UPLOAD_DIR)
    slug = models.SlugField(max_length=255, blank=True)
    pathname = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        print('__unicode__')
        print(str(self.file.name))
        print(self.file.name)
        return self.file.name
    
    def __str__(self):
        print('__str__')
        print(str(self.slug))
        print(self.slug)
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = str(self.file.name)
        super(FileUpload, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(FileUpload, self).delete(*args, **kwargs)
