# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-20 02:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_recommendedapp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendedapp',
            name='cateogry',
        ),
    ]
