# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-23 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20170123_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='passwords_users',
            field=models.CharField(default='', max_length=4096),
            preserve_default=False,
        ),
    ]
