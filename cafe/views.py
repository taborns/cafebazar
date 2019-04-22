# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from cafe.scrapper import scrap
from django.http import HttpResponse
from rest_framework import mixins, generics
from rest_framework.response import Response
from cafe import serializers, models
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

def scrapView(request):
    appDetails = scrap()
    return HttpResponse(appDetails)



class ListApps(generics.ListAPIView):
    
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer

class AppView(generics.RetrieveAPIView):
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'appID'

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

class CategoryAppView(generics.ListAPIView):
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer
    pagination_class = LimitOffsetPagination


    def list(self, request, categoryID):
        queryset = self.get_queryset()
        category= get_object_or_404(models.Category, pk=categoryID)
        apps = category.apps.all()
        page = self.paginate_queryset(apps)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(apps, many=True)

        return Response(serializer.data)

class SubCategoryAppView(generics.ListAPIView):
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer
    pagination_class = LimitOffsetPagination


    def list(self, request, subCategoryID):
        queryset = self.get_queryset()
        subCategory= get_object_or_404(models.SubCategory, pk=subCategoryID)
        apps = subCategory.apps.all()
        page = self.paginate_queryset(apps)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(apps, many=True)

        return Response(serializer.data)


class CategorySubCatView(generics.ListAPIView):
    queryset = models.SubCategory.objects.all()
    serializer_class = serializers.AppSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, categoryID):
        queryset = self.get_queryset()
        category= get_object_or_404(models.Category, pk=categoryID)
        subcategories = category.subcategories.all()
        serializer = serializers.SubCategorySerializer(subcategories, many=True)
        return Response(serializer.data)