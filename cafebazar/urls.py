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
from django.conf.urls import url, static
from django.contrib import admin
from cafe import views as cafe_views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^scrap/$', cafe_views.scrapView),
    url(r'^scrap/appurl/$', cafe_views.scrapAppsView),
    url(r'^scrap/appdetail/$', cafe_views.scrapAppDetailView),
    url(r'^scrap/subcat/$', cafe_views.scrapSubCatView),

    url('^apps/$', cafe_views.ListApps.as_view()),
    url('^categories/$', cafe_views.ListCategories.as_view()),
    url('^developers/$', cafe_views.ListDeveloperView.as_view()),
    url('^developer/(?P<developerID>\d+)/$', cafe_views.DetailDeveloperView.as_view()),
    url('^developer/(?P<developerID>\d+)/apps/$', cafe_views.DeveloperAppsView.as_view()),

    url('^subcategories/$', cafe_views.ListSubCategories.as_view()),
    url('^search/(?P<name>\w+)/$', cafe_views.SearchView.as_view()),
    url('^subcategories/(?P<categoryID>\d+)/$', cafe_views.CategorySubCatView.as_view()),
    url('^category/(?P<categoryID>\d+)/$', cafe_views.CategoryAppView.as_view()),
    url('^subcategory/(?P<subCategoryID>\d+)/$', cafe_views.SubCategoryAppView.as_view()),
    url('^app/(?P<packagename>[\w\.]+)/$', cafe_views.AppView.as_view()),
    url('^home/subcollections/$', cafe_views.HomeSubCollectionView.as_view()),
    url('^home/collections/$', cafe_views.HomeCollectionView.as_view()),
    url('^home/subcollections/(?P<collectionID>\d+)/$', cafe_views.HomeCollSubColl.as_view()),
    url('^home/subcollection/(?P<subCollectionID>\d+)/$', cafe_views.HomeSubCollApps.as_view()),
    url('^home/categories/$', cafe_views.HomeSubCatView.as_view()),
    url('^home/category/(?P<categoryID>\d+)/$', cafe_views.HomeSubCatApps.as_view()),

    url('^rank/scrap/$', cafe_views.rankScrapView),
    url('^rank/savecat/$', cafe_views.saveCatView),
    url('^rank/savefilter/$', cafe_views.saveAppFilterView),

    url('^rank/categories/$', cafe_views.RankCatView.as_view()),
    url('^rank/filters/$', cafe_views.RankFilterView.as_view()),
    url('^rank/apps/(?P<filterID>\d+)/(?P<categoryID>\d+)/$', cafe_views.RankAppView.as_view()),
    
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)