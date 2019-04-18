# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from cafe.scrapper import scrap
from django.http import HttpResponse
from rest_framework import mixins, generics
from rest_framework.response import Response
from cafe import serializers, models
# Create your views here.

def scrapView(request):
    appDetails = scrap()
    return HttpResponse(appDetails)



class ListApps(generics.ListAPIView):
    
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer

class ListCategories(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class ListSubCategories(generics.ListAPIView):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.SubCategorySerializer

class SearchView(generics.ListAPIView):
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer

    def list(self, request, name):
        queryset = self.get_queryset()
        apps = queryset.filter(name__startswith = name)
        serializer = serializers.AppSerializer(apps, many=True)
        return Response(serializer.data)
