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
    lookup_field = 'package_name'
    lookup_url_kwarg = 'packagename'

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

class HomeSubCatView(generics.ListAPIView):
    queryset = models.HomeSubCat.objects.all()
    serializer_class = serializers.HomeSubCatSerializer
    pagination_class = LimitOffsetPagination

class HomeCollectionView(generics.ListAPIView):
    queryset = models.HomeCollection.objects.all()
    serializer_class = serializers.HomeCollectionSerializer
    pagination_class = LimitOffsetPagination

class HomeCollSubColl(generics.ListAPIView):
    queryset = models.HomeSubCollection.objects.all()
    serializer_class = serializers.HomeSubCollectionSerializer
    pagination_class = LimitOffsetPagination
    
    def list(self, request, collectionID):
        queryset = self.get_queryset()
        collection= get_object_or_404(models.HomeCollection, pk=collectionID)
        subcollections = collection.subcollections.all()
        serializer = serializers.HomeSubCollectionSerializer(subcollections, many=True)
        return Response(serializer.data)

class HomeSubCatApps(generics.ListAPIView):
    queryset = models.HomeSubCat.objects.all()
    serializer_class = serializers.HomeSubCatSerializer
    pagination_class = LimitOffsetPagination
    
    def list(self, request,categoryID ):
        queryset = self.get_queryset()
        subcat= get_object_or_404(models.HomeSubCat, pk=categoryID)
        apps = subcat.apps.all()
        serializer = serializers.HomeAppSerializer(apps, many=True)
        return Response(serializer.data)

class HomeSubCollApps(generics.ListAPIView):
    queryset = models.HomeSubCollection.objects.all()
    serializer_class = serializers.HomeAppSerializer
    pagination_class = LimitOffsetPagination
    
    def list(self, request,subCollectionID ):
        queryset = self.get_queryset()
        subcollection= get_object_or_404(models.HomeSubCollection, pk=subCollectionID)
        apps = subcollection.apps.all()
        serializer = serializers.HomeAppSerializer(apps, many=True)
        return Response(serializer.data)


class HomeSubCollectionView(generics.ListAPIView):
    queryset = models.HomeSubCollection.objects.all()
    serializer_class = serializers.HomeSubCollectionSerializer
    pagination_class = LimitOffsetPagination

