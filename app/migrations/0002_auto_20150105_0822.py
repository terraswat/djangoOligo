# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='population_total',
            name='group',
            field=models.CharField(default=b'', max_length=80, verbose_name=b'Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='population_total',
            name='name',
            field=models.CharField(max_length=3, serialize=False, verbose_name=b'Name', primary_key=True),
            preserve_default=True,
        ),
    ]
