# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20160317_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='creation_date',
            field=models.DateField(null=True, verbose_name='Creation date', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='number_employees',
            field=models.IntegerField(default=1, verbose_name='Number of employees', choices=[(1, '1'), (2, 'Between 1 and 10'), (3, 'Between 10 and 50'), (4, 'More than 50')]),
        ),
        migrations.AddField(
            model_name='company',
            name='sales_revenue',
            field=models.IntegerField(default=1, verbose_name='Sales revenue', choices=[(1, 'Lower than 50.000 euros'), (2, 'Between 50.000 euros and 250.000 euros'), (3, 'Between 250.000 euros and 700.000 euros'), (4, 'Between 700.000 euros and 4.500.000 euros'), (5, 'More than 4.500.000 euros')]),
        ),
        migrations.AddField(
            model_name='company',
            name='website',
            field=models.URLField(null=True, verbose_name='Website', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='vat_number',
            field=models.CharField(max_length=10, unique=True, null=True, verbose_name='TVA number', blank=True),
        ),
    ]
