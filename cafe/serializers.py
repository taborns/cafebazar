from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from cafe import models

class AppSerializer(serializers.ModelSerializer):
    screenshots = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.App
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = '__all__'

class HomeAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HomeApp
        fields = '__all__'

class HomeSubCatSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HomeSubCat
        exclude = ('apps',)

    
class HomeSubCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HomeSubCollection
        exclude = ('apps',)

class HomeCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HomeCollection
        fields = '__all__'

class RankCatSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RankCat
        fields = '__all__'

class RankAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RankApp
        fields = '__all__'

class RankFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RankFilter
        fields = '__all__'


