# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 20:26
from __future__ import unicode_literals

import cafe.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_auto_20190418_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=cafe.models.NameField(max_length=100),
        ),
    ]
