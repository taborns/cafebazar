# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from cafe.scrapper import scrap
from cafe.ranks import rankScrap, saveCats, saveAppFilters
from django.http import HttpResponse
from rest_framework import mixins, generics
from rest_framework.response import Response
from cafe import serializers, models
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.

def scrapView(request, appcategories=True, gamecategories=True, subcategories=True, appUrls=True, homeStuff=True, appDetail=True ):
    appDetails = scrap(appcategories=True, gamecategories=True, subcategories=True, appUrls=True, homeStuff=True, appDetail=True)
    return HttpResponse(appDetails)

def screenshotView(request):
    getScreenShot()
    return HttpResponse('Done saving screenshot')
    
def scrapAppsView(request, appcategories=False, gamecategories=False, subcategories=False, appUrls=True, homeStuff=False, appDetail=False ):
    appDetails = scrap(appcategories=False, gamecategories=False, subcategories=False, appUrls=True, homeStuff=False, appDetail=False)
    return HttpResponse(appDetails)

def scrapAppDetailView(request, appcategories=False, gamecategories=False, subcategories=False, appUrls=False, homeStuff=False, appDetail=True ):
    appDetails = scrap( appcategories=False, gamecategories=False, subcategories=False, appUrls=False, homeStuff=False, appDetail=True )
    return HttpResponse(appDetails)

def scrapSubCatView(request, appcategories=False, gamecategories=False, subcategories=True, appUrls=False, homeStuff=False, appDetail=False ):
    appDetails = scrap( appcategories=False, gamecategories=False, subcategories=True, appUrls=False, homeStuff=False, appDetail=False )
    return HttpResponse(appDetails)

def saveCatView(request):
    saveCats()
    saveAppFilters()
    return HttpResponse('Done saving categories')

def rankScrapView(request):
    rankScrap()
    return HttpResponse('Done')

    

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
        serializer = serializers.AppSerializer(apps, many=True)
        return Response(serializer.data)

class HomeSubCollApps(generics.ListAPIView):
    queryset = models.HomeSubCollection.objects.all()
    serializer_class = serializers.AppSerializer
    pagination_class = LimitOffsetPagination
    
    def list(self, request,subCollectionID ):
        queryset = self.get_queryset()
        subcollection= get_object_or_404(models.HomeSubCollection, pk=subCollectionID)
        apps = subcollection.apps.all()
        serializer = serializers.AppSerializer(apps, many=True)
        return Response(serializer.data)


class HomeSubCollectionView(generics.ListAPIView):
    queryset = models.HomeSubCollection.objects.all()
    serializer_class = serializers.HomeSubCollectionSerializer
    pagination_class = LimitOffsetPagination


class RankCatView(generics.ListAPIView):
    queryset = models.RankCat.objects.all()
    serializer_class = serializers.RankCatSerializer
    pagination_class = LimitOffsetPagination




class RankFilterView(generics.ListAPIView):
    queryset = models.RankFilter.objects.all()
    serializer_class = serializers.RankFilterSerializer
    pagination_class = LimitOffsetPagination
    def list(self, request ):
        queryset = self.get_queryset()
        filters = models.RankFilter.objects.all()
        serializer = serializers.RankFilterSerializer(filters, many=True)
        return Response(serializer.data)



class RankAppView(generics.ListAPIView):
    queryset = models.RankApp.objects.all()
    serializer_class = serializers.RankAppSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, filterID, categoryID ):
        queryset = self.get_queryset()
        rankFilter = get_object_or_404(models.RankFilter, pk=filterID)
        rankCat = get_object_or_404(models.RankCat, pk=categoryID)
        apps = models.RankApp.objects.filter(rankfilter=rankFilter, rankcat=rankCat)
        serializer = serializers.RankAppSerializer(apps, many=True)
        return Response(serializer.data)


class ListDeveloperView(generics.ListAPIView):
    queryset = models.Developer.objects.all()
    serializer_class = serializers.DeveloperSerializer
    pagination_class = LimitOffsetPagination

class DetailDeveloperView(generics.RetrieveAPIView):
    queryset = models.Developer.objects.all()
    serializer_class = serializers.DeveloperSerializer
    pagination_class = LimitOffsetPagination

    lookup_field = 'pk'
    lookup_url_kwarg = 'developerID'

class DeveloperAppsView(generics.ListAPIView):
    queryset = models.App.objects.all()
    serializer_class = serializers.AppSerializer
    pagination_class = LimitOffsetPagination
    def list(self, request, developerID ):
        developer =  get_object_or_404(models.Developer, pk=developerID)
        serializer = serializers.AppSerializer(developer.apps.all(), many=True)
        return Response(serializer.data)


class RecommendedAppsView(generics.ListAPIView):
    queryset = models.RecommendedApp.objects.all()
    serializer_class = serializers.RecommendedAppSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, appType=None):
        recomApps = self.get_queryset()
        if appType:
            recomApps = recomApps.filter(app_type=appType)
            
        serializer = self.get_serializer_class()(recomApps, many=True)

        return Response( serializer.data)


