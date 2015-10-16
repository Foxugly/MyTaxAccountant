# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20151012_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='refer_trimester',
            field=models.ForeignKey(related_name='back_trimester', to='trimesters.Trimester', null=True),
        ),
    ]
