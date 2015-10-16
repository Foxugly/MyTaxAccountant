# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0002_year_refer_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='trimesters',
            field=models.ManyToManyField(to='trimesters.Trimester', blank=True),
        ),
    ]
