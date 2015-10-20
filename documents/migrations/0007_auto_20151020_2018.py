# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20151019_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='fiscal_id',
            field=models.CharField(max_length=100, null=True, verbose_name='Fiscal ID', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(null=True, verbose_name='description'),
        ),
    ]
