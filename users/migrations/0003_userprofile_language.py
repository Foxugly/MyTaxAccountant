# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151018_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='language',
            field=models.CharField(default=1, max_length=8, verbose_name='language', choices=[(b'fr', 'Francais'), (b'nl', 'Nederlands'), (b'en', 'English')]),
        ),
    ]
