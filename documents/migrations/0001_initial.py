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
                ('name', models.TextField()),
                ('size', models.IntegerField(null=True)),
                ('words', models.IntegerField(default=0, null=True)),
                ('done', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('filename', models.CharField(default=b'blank', max_length=100)),
                ('mininame', models.CharField(default=b'blank', max_length=100)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PendingDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=255)),
                ('doc', models.ForeignKey(to='documents.Document')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='pages',
            field=models.ManyToManyField(to='documents.Page'),
        ),
    ]
