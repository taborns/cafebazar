# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import base64

class NameObject:
    def __init__(self, val):

        self.val = base64.b64decode(base64.b64decode(val))
        
    def __unicode__(self):
        return self.val

# Create your models here.
class NameField(models.CharField):

    def __init__(self, *args, **kwargs):
        return super(NameField, self).__init__(*args, **kwargs)
    
    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, NameObject):
            return value

        if value is None:
            return value

        return NameObject(value)
    
    def get_prep_value(self, value):
        if value is None:
            return None
        return base64.b64encode(value)

class Category(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    url = models.URLField()
    category_type = models.IntegerField(choices=(
        (1, 'app'),
        (2, 'game')
    ))

    def __unicode__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    id = models.IntegerField(primary_key=True)
    category = models.ForeignKey('Category', related_name='subcategories')
    url = models.URLField()
    

class App(models.Model):
    cateogry = models.ForeignKey('Category', related_name='apps')
    sub_category = models.ForeignKey('SubCategory', related_name='apps')
    name = models.CharField(max_length=200)
    installs = models.CharField(max_length=200, null=True, blank=True)
    price = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    developer = models.ForeignKey('Developer', related_name='apps')
    size = models.CharField(max_length=200, null=True, blank=True)
    version = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField()
    icon = models.URLField()
    rating_total = models.CharField(max_length=200)
    rating_total_count = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, primary_key=True)

class Screenshot(models.Model):
    url = models.URLField()
    app = models.ForeignKey('App', related_name='screenshots')

    def __unicode__(self):
        return self.url

class Developer(models.Model):
    name = models.CharField(max_length=200)
    developerID = models.CharField(max_length=200)

class AppUrl(models.Model):
    url = models.URLField()
    category = models.IntegerField()
    subcategory = models.IntegerField()

class HomeSubCat(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    apps = models.ManyToManyField('HomeApp')

    def __unicode__(self):
        return self.name

class HomeCollection(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class HomeSubCollection(models.Model):
    name = models.CharField(max_length=200)
    collection = models.ForeignKey('HomeCollection', related_name='subcollections')
    apps = models.ManyToManyField('HomeApp')
    url = models.URLField()
    img = models.URLField()

    def __unicode__(self):
        return self.name

class HomeApp(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    url = models.URLField()
    icon = models.URLField()
    rating_total = models.CharField(max_length=200)
    rating_total_count = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200)


class RankCat(models.Model):
    catcode = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

class RankFilter(models.Model):
    name = models.CharField(max_length=200)
    filtercode = models.CharField(max_length=200)
   


class RankApp(models.Model):
    rankfilter = models.ForeignKey('RankFilter', related_name='apps')
    rankcat = models.ForeignKey('RankCat', related_name='apps')
    rank = models.IntegerField()
    name = models.CharField(max_length=200)
    packagename = models.CharField(max_length=200)
    icon = models.URLField()
    developer = models.CharField(max_length=200)
    rating = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    installs = models.CharField(max_length=200)


class RecommendedApp(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    version = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField()
    icon = models.URLField()
    rating_total = models.CharField(max_length=200)
    rating_total_count = models.CharField(max_length=200)
    package_name = models.CharField(max_length=200, primary_key=True)
    app_type = models.CharField(max_length=200, choices=(('recom', 'Recommended'), ('ad', 'Advertized')))