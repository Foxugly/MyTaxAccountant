# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20151020_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
    ]
