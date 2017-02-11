# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-11 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20170125_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=2048)),
                ('reason', models.CharField(max_length=32)),
                ('finished', models.BooleanField(db_index=True)),
            ],
        ),
    ]
