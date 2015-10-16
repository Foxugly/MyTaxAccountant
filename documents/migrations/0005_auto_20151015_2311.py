# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20151015_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pages',
            field=models.ManyToManyField(to='documents.Page', blank=True),
        ),
    ]
