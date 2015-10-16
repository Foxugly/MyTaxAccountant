# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20151012_0018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pendingdocument',
            name='doc',
        ),
        migrations.RemoveField(
            model_name='document',
            name='words',
        ),
        migrations.RemoveField(
            model_name='page',
            name='mininame',
        ),
        migrations.DeleteModel(
            name='PendingDocument',
        ),
    ]
