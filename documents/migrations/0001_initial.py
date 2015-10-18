# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(verbose_name='filename')),
                ('size', models.IntegerField(default=0, verbose_name='size')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='date')),
                ('description', models.TextField(verbose_name='description')),
                ('complete', models.BooleanField(default=False, verbose_name='complete')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(verbose_name='page number')),
                ('filename', models.CharField(default=b'blank', max_length=100, verbose_name='filename')),
                ('width', models.IntegerField(verbose_name='width')),
                ('height', models.IntegerField(verbose_name='height')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='pages',
            field=models.ManyToManyField(to='documents.Page', blank=True),
        ),
    ]
