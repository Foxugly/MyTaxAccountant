# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trimesters', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='refer_trimester',
            field=models.ForeignKey(related_name='back_trimester', to='trimesters.Trimester', null=True, on_delete=models.CASCADE),
        ),
    ]
