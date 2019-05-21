# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-21 11:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0007_remove_recommendedapp_cateogry'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendedapp',
            name='app_type',
            field=models.IntegerField(choices=[(1, 'Recommended'), (2, 'Advertized')], default=1),
            preserve_default=False,
        ),
    ]
