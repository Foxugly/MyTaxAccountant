# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_auto_20151012_0050'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='cat',
            field=models.ForeignKey(to='categories.TypeCategory'),
        ),
    ]
