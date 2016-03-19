# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0003_auto_20151018_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='admin',
            field=models.BooleanField(default=False, verbose_name='admin'),
        ),
    ]
