# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0002_auto_20151012_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='trimester',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='trimester',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='trimester',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
