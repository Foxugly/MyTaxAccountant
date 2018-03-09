# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0002_trimester_refer_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trimester',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', verbose_name='categories', blank=True),
        ),
        migrations.AlterField(
            model_name='trimester',
            name='refer_year',
            field=models.ForeignKey(related_name='back_year', verbose_name='year', to='years.Year', null=True, on_delete=models.CASCADE),
        ),
    ]
