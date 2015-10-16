# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_typecategory_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='typecategory',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
