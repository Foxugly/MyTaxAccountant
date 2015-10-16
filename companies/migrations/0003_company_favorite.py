# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20151012_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='favorite',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
