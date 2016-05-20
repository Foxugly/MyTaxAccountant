# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20160413_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='random',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
