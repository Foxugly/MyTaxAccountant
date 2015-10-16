# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_company_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='company',
            name='favorite',
            field=models.BooleanField(default=False),
        ),
    ]
