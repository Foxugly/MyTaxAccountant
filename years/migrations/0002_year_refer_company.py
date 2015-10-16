# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('years', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='refer_company',
            field=models.ForeignKey(related_name='back_company', to='companies.Company', null=True),
        ),
    ]
