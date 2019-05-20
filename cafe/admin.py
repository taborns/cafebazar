# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from cafe.models import RecommendedApp
# Register your models here.

class RecommendedAppModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_name')

admin.site.register(RecommendedApp, RecommendedAppModelAdmin)