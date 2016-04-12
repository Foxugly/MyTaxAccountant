# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
    ]
