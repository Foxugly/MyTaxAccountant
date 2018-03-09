# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('documents', '0002_page_refer_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='refer_category',
            field=models.ForeignKey(related_name='back_category', to='categories.Category', null=True, on_delete=models.CASCADE),
        ),
    ]
