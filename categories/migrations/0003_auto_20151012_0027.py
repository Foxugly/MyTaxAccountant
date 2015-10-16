# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_refer_trimester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='documents',
            field=models.ManyToManyField(to='documents.Document', blank=True),
        ),
    ]
