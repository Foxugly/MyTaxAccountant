# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '__first__'),
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('fiscal_year', models.ForeignKey(to='utils.FiscalYear')),
                ('trimesters', models.ManyToManyField(to='trimesters.Trimester')),
            ],
        ),
    ]
