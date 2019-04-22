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
    name = models.CharField(max_length=100)
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
    developer = models.CharField(max_length=200)
    developer_url = models.URLField(max_length=200)
    size = models.CharField(max_length=200, null=True, blank=True)
    version = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField()
    icon = models.URLField()


class Screenshot(models.Model):
    url = models.URLField()
    app = models.ForeignKey('App')
class AppUrl(models.Model):
    url = models.URLField()
    category = models.IntegerField()
    subcategory = models.IntegerField()