# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0003_auto_20190429_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='homesubcollection',
            name='img',
            field=models.URLField(default='https://google.com'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homesubcollection',
            name='url',
            field=models.URLField(default='https://google.com'),
            preserve_default=False,
        ),
    ]
