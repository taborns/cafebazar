# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-09 12:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0014_screenshot_original_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appurl',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='cafe.Category'),
        ),
        migrations.AlterField(
            model_name='appurl',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='cafe.SubCategory'),
        ),
    ]
