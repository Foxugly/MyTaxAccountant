# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='refer_document',
            field=models.ForeignKey(related_name='back_document', to='documents.Document', null=True),
        ),
    ]
