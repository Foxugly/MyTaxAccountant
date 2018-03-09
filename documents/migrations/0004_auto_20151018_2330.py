# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_document_refer_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='refer_category',
            field=models.ForeignKey(related_name='back_category', verbose_name='category', to='categories.Category', null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='page',
            name='refer_document',
            field=models.ForeignKey(related_name='back_document', verbose_name='document', to='documents.Document', null=True, on_delete=models.CASCADE),
        ),
    ]
