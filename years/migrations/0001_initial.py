# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '__first__'),
        ('trimesters', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('favorite', models.BooleanField(default=False, verbose_name='favorite')),
                ('fiscal_year', models.ForeignKey(to='utils.FiscalYear', on_delete=models.CASCADE)),
                ('trimesters', models.ManyToManyField(to='trimesters.Trimester', blank=True)),
            ],
        ),
    ]
