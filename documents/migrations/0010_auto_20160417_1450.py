# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_document_lock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='fiscal_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Fiscal ID', validators=[django.core.validators.RegexValidator(regex=b'^[0-9]{8}$', message="Fiscal ID must be entered in the format: 'YYYYNNNN' where YYYY is the year and NNNN the id. Only 8 digits allowed.", code=b'invalid_ID_fiscal')]),
        ),
    ]
