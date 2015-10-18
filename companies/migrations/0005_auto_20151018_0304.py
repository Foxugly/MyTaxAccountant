# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20151012_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address_1',
            field=models.CharField(max_length=128, null=True, verbose_name='address', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.ForeignKey(to='utils.Country', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='vat_number',
            field=models.CharField(max_length=10, unique=True, null=True, verbose_name='TVA number'),
        ),
    ]
