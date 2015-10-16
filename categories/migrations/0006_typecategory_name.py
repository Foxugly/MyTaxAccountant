# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20151015_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='typecategory',
            name='name',
            field=models.CharField(default=0, max_length=128, verbose_name='Type of documents'),
            preserve_default=False,
        ),
    ]
