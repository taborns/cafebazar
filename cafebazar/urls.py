"""cafebazar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cafe import views as cafe_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^scrap/$', cafe_views.scrapView),
    url('^apps/$', cafe_views.ListApps.as_view()),
    url('^categories/$', cafe_views.ListCategories.as_view()),
    url('^subcategories/$', cafe_views.ListSubCategories.as_view()),
    url('^search/(?P<name>\w+)/$', cafe_views.SearchView.as_view()),
    url('^subcategories/(?P<categoryID>\d+)/$', cafe_views.CategorySubCatView.as_view()),
    url('^category/(?P<categoryID>\d+)/$', cafe_views.CategoryAppView.as_view()),
    url('^subcategory/(?P<subCategoryID>\d+)/$', cafe_views.SubCategoryAppView.as_view()),
    url('^app/(?P<appID>\d+)/$', cafe_views.AppView.as_view()),
    
]
