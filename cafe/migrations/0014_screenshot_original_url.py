# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-03 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0013_auto_20190603_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='screenshot',
            name='original_url',
            field=models.URLField(default='https://google.com'),
            preserve_default=False,
        ),
    ]
