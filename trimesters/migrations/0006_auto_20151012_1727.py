# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0005_trimester_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trimester',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
    ]
