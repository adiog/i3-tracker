# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('datetime_start', models.DateTimeField()),
                ('datetime_stop', models.DateTimeField()),
            ],
        ),
    ]
