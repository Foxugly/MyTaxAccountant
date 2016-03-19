# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiscalyear',
            name='name',
            field=models.TextField(max_length=20, verbose_name='Fiscal year'),
        ),
    ]
