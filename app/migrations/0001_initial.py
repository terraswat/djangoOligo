# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Array',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, verbose_name=b'Name', primary_key=True)),
                ('descr', models.CharField(max_length=255, verbose_name=b'Description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primer', models.CharField(max_length=255, verbose_name=b'Primer')),
                ('rating', models.IntegerField(default=0, verbose_name=b'Rating')),
                ('text', models.TextField(max_length=2047, verbose_name=b'Comment', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, verbose_name=b'Name', primary_key=True)),
                ('descr', models.CharField(max_length=255, verbose_name=b'Description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Oligo',
            fields=[
                ('primer', models.CharField(max_length=255, serialize=False, verbose_name=b"Primer (5'-> 3')", primary_key=True)),
                ('family', models.CharField(max_length=255, verbose_name=b'Satellite Family')),
                ('array', models.CharField(max_length=255, verbose_name=b'Array Name')),
                ('frequency', models.FloatField(default=0, verbose_name=b'Frequency')),
                ('chr', models.CharField(default=b'1', max_length=2, verbose_name=b'Human Chromosome')),
                ('bestStart', models.IntegerField(default=0, verbose_name=b'Best Start')),
                ('bestEnd', models.IntegerField(default=0, verbose_name=b'Best End')),
                ('location', models.CharField(max_length=255, verbose_name=b'Location with 10% le')),
                ('genomeBrowser', models.CharField(max_length=1023, null=True, verbose_name=b'UCSC Genome Browser', blank=True)),
                ('citation', models.CharField(max_length=2047, null=True, verbose_name=b'Citations', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primer', models.CharField(max_length=255, verbose_name=b'Primer')),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('count', models.IntegerField(default=0, verbose_name=b'Count')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Population_total',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, verbose_name=b'Name', primary_key=True)),
                ('count', models.IntegerField(default=0, verbose_name=b'Count')),
                ('order', models.IntegerField(default=0, verbose_name=b'Order of Appearance')),
                ('descr', models.CharField(max_length=255, verbose_name=b'Description')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
