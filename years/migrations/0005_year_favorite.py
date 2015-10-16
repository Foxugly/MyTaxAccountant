# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0004_auto_20151012_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='favorite',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
