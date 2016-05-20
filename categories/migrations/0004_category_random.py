# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20151018_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='random',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
