# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0004_year_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='random',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
