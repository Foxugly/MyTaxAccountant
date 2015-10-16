# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('years', '0001_initial'),
        ('categories', '0001_initial'),
        ('companies', '0001_initial'),
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='refer_category',
            field=models.ForeignKey(related_name='back_category', to='categories.Category', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='refer_company',
            field=models.ForeignKey(related_name='back_company', to='companies.Company', null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='refer_year',
            field=models.ForeignKey(related_name='back_year', to='years.Year', null=True),
        ),
    ]
