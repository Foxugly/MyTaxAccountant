# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20151019_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date'),
        ),
    ]
