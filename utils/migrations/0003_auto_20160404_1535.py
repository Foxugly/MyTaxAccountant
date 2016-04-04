# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20160317_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiscalyear',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fiscalyear',
            name='init',
            field=models.BooleanField(default=False),
        ),
    ]
