# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20151020_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='lock',
            field=models.BooleanField(default=False, verbose_name='locked'),
        ),
    ]
