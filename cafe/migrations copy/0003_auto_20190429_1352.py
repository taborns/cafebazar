# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-29 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_auto_20190429_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homecollection',
            name='img',
        ),
        migrations.RemoveField(
            model_name='homecollection',
            name='url',
        ),
        migrations.AlterField(
            model_name='homesubcollection',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcollections', to='cafe.HomeCollection'),
        ),
    ]
