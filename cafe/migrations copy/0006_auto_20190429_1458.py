# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_auto_20190429_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeapps',
            name='cateogry',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='description',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='developer',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='developer_url',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='installs',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='size',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='sub_category',
        ),
        migrations.RemoveField(
            model_name='homeapps',
            name='version',
        ),
    ]
