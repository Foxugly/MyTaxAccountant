# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_auto_20160404_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateTrimester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(null=True, verbose_name='trimester number')),
                ('favorite', models.BooleanField(default=False, verbose_name='favorite')),
                ('start_date', models.DateField(null=True, verbose_name='start date')),
                ('year', models.ForeignKey(to='utils.FiscalYear', null=True, on_delete=models.CASCADE)),
            ],
        ),
    ]
