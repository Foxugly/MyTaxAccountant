# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0003_auto_20151012_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trimester',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
