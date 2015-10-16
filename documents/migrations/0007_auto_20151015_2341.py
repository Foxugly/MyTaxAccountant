# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_remove_document_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='size',
            field=models.IntegerField(default=0),
        ),
    ]
