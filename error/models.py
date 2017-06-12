from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Error(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(_('date'), default=timezone.now, null=False)
    detail = models.TextField(_('description'), blank=True, null=True)
