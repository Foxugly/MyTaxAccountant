# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0004_auto_20151012_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='trimester',
            name='favorite',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
