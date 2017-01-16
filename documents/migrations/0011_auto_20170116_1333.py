# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20160417_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='filename',
            field=models.CharField(default=b'blank', max_length=255, verbose_name='filename'),
        ),
    ]
