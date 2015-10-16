# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0002_year_refer_company'),
        ('trimesters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trimester',
            name='refer_year',
            field=models.ForeignKey(related_name='back_year', to='years.Year', null=True),
        ),
        migrations.AlterField(
            model_name='trimester',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
