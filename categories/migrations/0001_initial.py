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
                ('cat', models.CharField(default=b'O', max_length=1, choices=[(b'S', 'Sales'), (b'I', 'Invoice'), (b'B', 'Bank'), (b'O', 'Others')])),
                ('documents', models.ManyToManyField(to='documents.Document')),
            ],
        ),
    ]
