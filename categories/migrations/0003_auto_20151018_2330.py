# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_refer_trimester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='documents',
            field=models.ManyToManyField(to='documents.Document', verbose_name='documents', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='refer_trimester',
            field=models.ForeignKey(related_name='back_trimester', verbose_name='trimester', to='trimesters.Trimester', null=True, on_delete=models.CASCADE),
        ),
    ]
