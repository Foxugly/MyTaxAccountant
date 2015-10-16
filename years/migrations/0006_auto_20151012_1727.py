# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0005_year_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
    ]
