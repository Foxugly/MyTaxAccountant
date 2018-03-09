# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '__first__'),
        ('years', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(verbose_name='Name of the company')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(null=True, verbose_name='Description of the company')),
                ('vat_number', models.CharField(max_length=10, unique=True, null=True, verbose_name='TVA number')),
                ('address_1', models.CharField(max_length=128, null=True, verbose_name='address', blank=True)),
                ('address_2', models.CharField(max_length=128, null=True, verbose_name="address cont'd", blank=True)),
                ('zip_code', models.CharField(max_length=5, null=True, verbose_name='zip code', blank=True)),
                ('city', models.CharField(max_length=128, null=True, verbose_name='city', blank=True)),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('favorite', models.BooleanField(default=False, verbose_name='favorite')),
                ('country', models.ForeignKey(to='utils.Country', blank=True, on_delete=models.CASCADE)),
                ('years', models.ManyToManyField(to='years.Year', blank=True)),
            ],
        ),
    ]
