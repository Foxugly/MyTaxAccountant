# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20151015_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
