# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-03 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0012_auto_20190603_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homesubcollection',
            name='apps',
            field=models.ManyToManyField(to='cafe.App'),
        ),
    ]
