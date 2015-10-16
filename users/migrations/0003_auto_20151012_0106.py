# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151012_0029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='company',
            new_name='companies',
        ),
    ]
