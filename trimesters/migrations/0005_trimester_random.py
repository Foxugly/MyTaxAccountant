# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0004_auto_20160404_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='trimester',
            name='random',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
