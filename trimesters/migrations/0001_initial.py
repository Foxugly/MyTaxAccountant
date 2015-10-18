# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trimester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, verbose_name='trimester number')),
                ('start_date', models.DateField(null=True, verbose_name='start date')),
                ('end_date', models.DateField(null=True, verbose_name='end_date', blank=True)),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('favorite', models.BooleanField(default=False, verbose_name='favorite')),
                ('categories', models.ManyToManyField(to='categories.Category', blank=True)),
            ],
        ),
    ]
