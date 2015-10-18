# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
            ],
        ),
        migrations.CreateModel(
            name='TypeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Type of documents')),
                ('priority', models.IntegerField(unique=True, verbose_name='Priority')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='cat',
            field=models.ForeignKey(to='categories.TypeCategory'),
        ),
        migrations.AddField(
            model_name='category',
            name='documents',
            field=models.ManyToManyField(to='documents.Document', blank=True),
        ),
    ]
