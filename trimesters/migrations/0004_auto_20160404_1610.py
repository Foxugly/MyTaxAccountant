# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_templatetrimester'),
        ('trimesters', '0003_auto_20151018_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trimester',
            name='number',
        ),
        migrations.AddField(
            model_name='trimester',
            name='template',
            field=models.ForeignKey(blank=True, to='utils.TemplateTrimester', null=True),
        ),
    ]
