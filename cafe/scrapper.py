import requests
from bs4 import BeautifulSoup
import models
import base64
import urlparse
from urllib import urlencode
from scrapFuncs import *
from django.db.models import Q
from multiprocessing.pool import ThreadPool


HOME_CAT_ID = 0
HOME_URL =  "https://cafebazaar.ir"

thread_count = 20
thread_pool = ThreadPool(processes=thread_count) 
 

class AppImageHandler:
    def __init__(self, app):
        self.app = app

    def handle(self, url):
        screenshot = models.Screenshot(app=self.app, url=url)
        print "HANDING SCREENSHOT"
        self.app.screenshots.add( screenshot  )

    def handleIcon(self, url):
        self.app.icon = url
        self.app.save()


def saveCategories(category_type=1):
    categories_url = HOME_URL + "/cat/?partial=true"
    html = requests.get(categories_url)

    soup = BeautifulSoup(html.text, 'lxml')
    #get list of app categories 
    all_apps_ul = soup.find_all('ul')[category_type-1]
    all_apps = all_apps_ul.find_all('a')
    home_category = {'id' : HOME_CAT_ID, 'text' : 'home', 'url' : '/' }
    cafe_bazar_categories = []
    category_names = []
    for app in all_apps:
        app_name = app.get_text().encode('utf-8').strip()
        app_url = (app.get('href')).strip()
        try:
            category= models.Category.objects.get(name=app_name, category_type=category_type)
            category.url = app_url
            category.save()
        except Exception as e:
            category = models.Category.objects.create(**{ 'category_type' : category_type, 'name' : app_name, 'url' : app_url})
        
        cafe_bazar_categories.append(category)

        category_names.append( app_name )
    
    #remove categories not in the list 
    models.Category.objects.filter( ~Q( name__in=category_names ), category_type=category_type).delete()

    return cafe_bazar_categories  

#retusn the categories and collections from the cafebazar homepage 
def get_cafeBazarHomeCats():
    #home categories and sub categories 
    home_category = {'id' : HOME_CAT_ID, 'text' : 'home', 'url' : '/' }

    sub_category_link_sel = ".msht-row-more a"
    sub_category_selector = ".msht-row-head .msht-row-title"

    home_url =  HOME_URL + home_category['url']
    home_html = requests.get(home_url)
    home_soup = BeautifulSoup(home_html.text, 'lxml')
    home_sub_categories = []
    home_collections = {}
    for sub_category_selected in home_soup.select(sub_category_selector):
        a_link = sub_category_selected.findNext('span').find('a')
        sub_lbl = sub_category_selected.get_text().encode('utf-8').strip()
        category_values = {'name' : sub_lbl}
        
        if a_link:
            category_values['url'] = a_link.get('href').encode('utf-8').strip()
            home_sub_categories.append(category_values)
        
        else:
            collection_wrapper = sub_category_selected.parent.findNext('div')
            sub_collections = collection_wrapper.select('.msht-promo a')
            home_collections[sub_lbl] = []
            for sub_collection in sub_collections:
                image_url = 'https:' + sub_collection.findNext('picture').find('img').get('src')
                collection_url = sub_collection.get('href').encode('utf-8').strip()
                collection_soup = BeautifulSoup(requests.get(HOME_URL+ collection_url).text, 'lxml')
                h1s = collection_soup.select('.container-head h1')
                if len(h1s) > 0:
                    h1 = h1s[0]
                    sub_col_name = h1.get_text().encode('utf-8').strip()
                    home_collections[sub_lbl].append( {'name' : sub_col_name, 'url' : collection_url , 'img' : image_url} )
    
    return home_sub_categories, home_collections

def homeCatSave(home_sub_categories):
    cat_pks = []
    def getAppDetailCat(homeSubCatAppUrlObj, homeSubCatObject):
        homeApp = getAppDetail(homeSubCatAppUrlObj)
        print "Home category App ", homeSubCatObject.name, homeSubCatObject.pk, homeApp.package_name
        if homeApp:
            homeSubCatObject.apps.add(homeApp)
            
    for home_sub_category in home_sub_categories:
        
        homeSubCatObject = models.HomeSubCat.objects.filter(name = home_sub_category.get('name'))
        homeSubCatObject.update(**home_sub_category)
        homeSubCatObject = homeSubCatObject.first()
        if not homeSubCatObject:
            homeSubCatObject = models.HomeSubCat.objects.create(**home_sub_category)
        
        cat_pks.append(homeSubCatObject.pk)

        homeSubCatObject.apps.clear()

        homeSubCatAppUrls = getAllApps( HOME_URL + home_sub_category['url'] )
        homeSubCatAppUrlObjs = []
        for homeSubCatAppUrl in homeSubCatAppUrls:
            homeSubCatAppUrlObjs.append(models.AppUrl(url= homeSubCatAppUrl, category=0, subcategory=0) )
        
        for homeSubCatAppUrlObj in homeSubCatAppUrlObjs:
            thread_pool.apply_async(getAppDetailCat, args=(homeSubCatAppUrlObj, homeSubCatObject))


    models.HomeSubCat.objects.filter(~Q(pk__in=cat_pks)).delete()

def homeCollSave(home_collections):
    home_collection_pks = []
    home_app_package_names = []
    
    def getAppDetailColl(subcollection_app_url_obj, homeSubCollectionObject):
        homeApp = getAppDetail(subcollection_app_url_obj)
        print "Collection save", homeApp.name, homeApp.pk, homeSubCollectionObject.name, homeSubCollectionObject.pk
        if homeApp:
            homeSubCollectionObject.apps.add(homeApp)
            home_app_package_names.append(homeApp.package_name)
    
    for home_collection_name in home_collections:
        home_subcollections = home_collections[home_collection_name]

        home_collection_object = models.HomeCollection.objects.filter(name = home_collection_name).first()
        if not home_collection_object:
            print "#### ****  HOME COLLECTION ERR"
            home_collection_object = models.HomeCollection.objects.create(name=home_collection_name)
        
        home_collection_pks.append( home_collection_object.pk )

        home_subcollection_pks = []
        for home_subcollection in home_subcollections:
            home_subcollection['collection'] = home_collection_object

            homeSubCollectionObject =home_collection_object.subcollections.filter(name=home_subcollection.get('name'))
            homeSubCollectionObject.update( **home_subcollection)
            homeSubCollectionObject = homeSubCollectionObject.first()
            if not homeSubCollectionObject:
                print "#### ****  HOME SUB COLLECTION ERR"

                homeSubCollectionObject = models.HomeSubCollection.objects.create(**home_subcollection)
            homeSubCollectionObject.apps.clear()

            home_subcollection_pks.append(homeSubCollectionObject.pk)

            subcollection_app_urls = getAllApps(HOME_URL + home_subcollection['url'])
            subcollection_app_url_objs = []

            for subcollection_app_url in subcollection_app_urls:
                subcollection_app_url = HOME_URL+ subcollection_app_url

            for subcollection_app_url in subcollection_app_urls:
                subcollection_app_url_objs.append(models.AppUrl(url= subcollection_app_url, category=0, subcategory=0) )
        
            for subcollection_app_url_obj in subcollection_app_url_objs:
                thread_pool.apply_async(getAppDetailColl, args=(subcollection_app_url_obj,  homeSubCollectionObject) )
        
        home_collection_object.subcollections.filter(~Q(pk__in=home_subcollection_pks)).delete()

    models.HomeCollection.objects.filter( ~Q( pk__in=home_collection_pks)).delete()

def addSubCategories(categories):
     #for each categories retrieve every sub categories 
    sub_categories = []
    sub_category_pks = []
    sub_category_collections = {}
    sub_category_selector = ".msht-row-head .msht-row-title"

    for index, category in enumerate(categories):
        print "sub category add", category.name
        full_url =  HOME_URL + category.url
        html = requests.get(full_url)
        
        soup = BeautifulSoup(html.text, 'lxml')
    
        sub_categories_label = []
        for sub_category_selected in soup.select(sub_category_selector):
            a_link = sub_category_selected.findNext('span').find('a')
            sub_lbl = sub_category_selected.get_text().encode('utf-8').strip()
            category_values = [sub_lbl]
            
            if a_link:
                category_values.append(a_link.get('href').encode('utf-8').strip())
                sub_categories_label.append(category_values)
        subCatNames = []
        for label, url in sub_categories_label:
            subCatNames.append( label )

            subcat = category.subcategories.filter(name=label)
            subcat.update(url=url)
            subcat = subcat.first()

            if not subcat:
                print  category.pk, "CAT PK"
                subcat = models.SubCategory(**{ 'name' : label, 'url' : url})
                subcat.category = category

                subcat.save() 
                
            sub_categories.append( subcat )
            sub_category_pks.append(subcat.pk)
    
        category.subcategories.filter( ~Q(pk__in=sub_category_pks)).delete()

    return sub_categories

def getAppURLS(sub_categories):
    app_url_urls = []
    app_urls = set()

    for sub_category in sub_categories:
        print "APP URL", sub_category.category.name, sub_category.name
        current_page = 0

        #to get full app list change language to english 
        sub_category_url = "https://cafebazaar.ir/" + sub_category.url + "?&p=" + str(current_page) + "&partial=true"
        params = {'l' : 'fa'}
        url_parts = list(urlparse.urlparse(sub_category_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        sub_category_url= urlparse.urlunparse(url_parts)

        html = requests.get(sub_category_url)
        soup = BeautifulSoup(html.text, 'lxml')
        apps = soup.select(".msht-app-list a")
        while len(apps)>0:
            current_page += PAGE_INC
            html = requests.get(sub_category_url)
            soup = BeautifulSoup(html.text, 'lxml')

            for app in apps:
                appURL =  (app.get('href')).encode('utf-8').strip()
                try:
                    app_url = models.AppUrl.objects.get(url=appURL)
                except:
                    app_url = models.AppUrl.objects.create(**{ 'category' : sub_category.category.pk, 'url' : appURL, 'subcategory' : sub_category.pk })
                
                app_url_urls.append(appURL)

            app_urls.add( app_url )

            sub_category_url = "https://cafebazaar.ir/" + sub_category.url + "?&p=" + str(current_page) + "&partial=true"
            html = requests.get(sub_category_url)
            soup = BeautifulSoup(html.text, 'lxml')
            apps = soup.select(".msht-app-list a")
        
    models.AppUrl.objects.filter(~Q(url__in=app_url_urls)).delete()

    return app_urls

def getAppDetail(app_url_):        
    counter = 0
    app_url_en = HOME_URL + app_url_.url
    print "Parsing app detail : ", app_url_en
    #change app to iran lanuage so to get information in iran lanuage
    params = {'l' : 'fa'}
    app_url = ""
    url_parts = list(urlparse.urlparse(app_url_en))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    app_url= urlparse.urlunparse(url_parts)
    counter+=1

    package_name = app_url.split("/")[-2]
    
    #check if app already saved. Pass if it is saved
    try:
        app = models.App.objects.get(package_name=package_name)
        print "APP ALREADY SAVED"
        return app
    except:
        pass

    html = requests.get(app_url)
    soup = BeautifulSoup(html.text, 'lxml')
    html_en = requests.get(app_url_en)
    soup_en = BeautifulSoup(html_en.text, 'lxml')

    icon_sel = ".app-img"
    title_sel = ".app-name h1"

    dev_sel = ".dev a"
    price_sel = ".price a"
    screen_shots = ".screenshot-holder .screenshot-wrp a"
    description_sel = ".app-container .row .col-sm-8 .rtl" #0th element 
    app_attributes = ".col-sm-4 div span"
    rating_total = ".rating-total"
    rating_total_count = ".rating-total-count"
    categoryID = 6
    installsID = 9
    sizeID = 11
    versionID = 13
    app_detail = {}
    try:
        app_detail['icon'] = "https:" + soup.select(icon_sel)[0].get('src')
        app_detail['name'] = (soup.select(title_sel)[0].get_text()).encode('utf-8').strip()
        developer = {}
        developer['name'] = (soup.select(dev_sel)[0].get_text()).encode('utf-8').strip()
        developerURL  = soup.select(dev_sel)[0].get('href')
        developer['developerID'] = developerURL.split('/')[-2]
        developer, created = models.Developer.objects.get_or_create(**developer)
        app_detail['developer'] = developer
        app_detail['price'] =(soup.select(price_sel)[0].get_text()).encode('utf-8').strip()
        screenshots = {"https:" + screenshot.get('href') for screenshot in soup.select(screen_shots)}
        app_category_name = (soup.select(app_attributes)[categoryID].get_text()).encode('utf-8').strip()
        app_category = models.Category.objects.get(name=app_category_name)
        app_detail['cateogry'] = app_category
        app_detail['sub_category'] = app_category.subcategories.first()
        app_detail['rating_total'] = soup_en.select(rating_total)[0].get_text().encode('utf-8').strip()
        app_detail['rating_total_count'] = soup_en.select(rating_total_count)[0].get_text().encode('utf-8').strip()
        app_detail['url'] = app_url
        app_detail['package_name'] = app_url.split("/")[-2]
    except Exception as e:
        return
    try:
        app_detail['description'] = (soup.select(description_sel)[0].get_text()).encode('utf-8').strip()
    except Exception as e:
        pass

    try:
        app_detail['installs'] = (soup.select(app_attributes)[installsID].get_text()).encode('utf-8').strip()
    except:
        pass
    try:
        app_detail['size'] = (soup.select(app_attributes)[sizeID].get_text()).encode('utf-8').strip()
    except:
        pass
    try:
        app_detail['version'] = (soup.select(app_attributes)[versionID].get_text()).encode('utf-8').strip()
    except:
        pass
    
    try:
        app = models.App.objects.get(package_name=app_url.split("/")[-2])
        app.update(**app_detail)
    except:
        app = models.App(**app_detail)
        app.save()
    
    found_screenshots = set()
    for screenshoturl in screenshots:
        found = False
        for app_screenshot in app.screenshots.all():
            if screenshoturl == app_screenshot.original_url:
                found_screenshots.add( screenshoturl )
                break
        
    app.screenshots.filter(~Q( url__in=screenshots )).delete()
    appImageHandler = AppImageHandler(app)

    new_screenshots = screenshots.difference( found_screenshots)
    #handle screenshot compression 
    for new_screenshot in new_screenshots:
        screenshot_image_name = generateRandomName( new_screenshot,  'screenshot-')
        screenshot = models.Screenshot.objects.create(app=app, url=screenshot_image_name, original_url=new_screenshot)
        app.screenshots.add( screenshot  )

    icon_image_name = generateRandomName(app_detail['icon'])
    app.icon = icon_image_name
    app.save()
    convertWebp(app_detail['icon'], icon_image_name)
    
    return app

def getScreenShot():
    screenshots = models.Screenshot.objects.all()  
    for screenshot in screenshots:
        thread_pool.apply_async(convertWebp, (screenshot.original_url, screenshot.url, (500,400)) )
    
    thread_pool.close() # After all threads started we close the pool
    thread_pool.join() # And wait until all threads are done

def scrap(skipFirst=False, appcategories=True, gamecategories=True, subcategories=True, appUrls=True, homeStuff=True, appDetail=True):

    PAGE_INC = 24
    categories_url = "https://cafebazaar.ir/cat/?partial=true"
    html = requests.get(categories_url)

    soup = BeautifulSoup(html.text, 'lxml')
    if appcategories:
        #get list of app categories 
        home_category = {'id' : HOME_CAT_ID, 'text' : 'home', 'url' : '/' }
        app_categories = saveCategories(1)
        game_categories = saveCategories(2)
        categories = app_categories + game_categories
    else:
        categories = models.Category.objects.all()

    if subcategories:
        #for each categories retrieve every sub categories 
        sub_categories = addSubCategories(categories)
    else:
        sub_categories = models.SubCategory.objects.all()
    
    #sub_categories = models.SubCategory.objects.all()
    
    #get apps in sub category 
    app_urls = set()


    #home setting
    if homeStuff:
        print "Scrapping home stuff"
        home_sub_categories, home_collections = get_cafeBazarHomeCats()
        print "DONE SUB CATEGORING"
        homeCatSave( home_sub_categories)
        print "DONE HOME CAT SAVE"
        homeCollSave(home_collections)
    print "HOME STUFF"
    
    
    if appUrls:
        print "APP URLS"
        app_urls = getAppURLS(sub_categories)
    else:
        app_urls =  models.AppUrl.objects.all()


    #app_urls =  models.AppUrl.objects.all()
    #retrieve app detail 
    if appDetail:
        counter = 0
        for app_url in app_urls:
            thread_pool.apply_async(getAppDetail, (app_url,))
            counter+=1
    
    thread_pool.close() # After all threads started we close the pool
    thread_pool.join() # And wait until all threads are done



#import json
#print(json.dumps( app_details ))


        

