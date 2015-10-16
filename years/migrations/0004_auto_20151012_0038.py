# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0003_auto_20151012_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='refer_company',
            field=models.ForeignKey(related_name='back_company', blank=True, to='companies.Company', null=True),
        ),
    ]
