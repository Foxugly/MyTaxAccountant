# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20151018_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 17, 16, 18, 449095, tzinfo=utc), verbose_name='date'),
        ),
    ]
