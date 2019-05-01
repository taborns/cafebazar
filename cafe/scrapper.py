import requests
from bs4 import BeautifulSoup
import models
import base64
import urlparse
from urllib import urlencode
from scrapFuncs import *

HOME_CAT_ID = -10
HOME_URL =  "https://cafebazaar.ir"
def scrap(skipFirst=False, appcategories=True, gamecategories=True, subcategories=True, appUrls=True, homeStuff=True, appDetail=True):
    PAGE_INC = 24
    categories_url = "https://cafebazaar.ir/cat/?partial=true"
    html = requests.get(categories_url)

    soup = BeautifulSoup(html.text, 'lxml')

    #get list of app categories 
    all_apps_ul = soup.find('ul')
    all_apps = all_apps_ul.find_all('a')
    home_category = {'id' : HOME_CAT_ID, 'text' : 'home', 'url' : '/' }
    app_categories = []
    if appcategories:
        for index, app in enumerate(all_apps):
            app_categories.append({'id' : index+1, 'text' :app.get_text().encode('utf-8').strip(), 'url' : (app.get('href')).strip() }) 
            category = models.Category(**{'id' : index+1, 'category_type' : 1, 'name' :app.get_text().encode('utf-8').strip(), 'url' : (app.get('href')).strip() })
            category.save()        
    

    #get list of game cateogries
    all_games_ul = soup.find_all('ul')[1]
    all_games = all_games_ul.find_all('a')
    game_categories = []
    
    if gamecategories:
        counter = models.Category.objects.count() + 1
        for index, game in enumerate(all_games):
            game_categories.append({'id' : index+counter, 'text' : (game.get_text()).encode('utf-8').strip(), 'url' : (game.get('href')).strip() }) 
            models.Category.objects.create(**{'id' : index+counter,'category_type' : 2, 'name' : (game.get_text()).encode('utf-8').strip(), 'url' : (game.get('href')).strip() })

    print "EHRE DONE",subcategories

    if not appcategories and not gamecategories:
        categories = [ {'id' : category.id, 'text' : category.name, 'category_type' : category.category_type, 'url' : category.url } for category in  models.Category.objects.all()]
    else:
        categories = app_categories + game_categories
    sub_category_selector = ".msht-row-head .msht-row-title"
    sub_category_link_sel = ".msht-row-more a"

    #home setting
    if homeStuff:
        #home categories and sub categories 
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

        for home_sub_category in home_sub_categories:
            homeSubCatObject = models.HomeSubCat.objects.create(**home_sub_category)
            homeSubCatAppUrls = getAllApps( HOME_URL + home_sub_category['url'] )
            for homeSubCatAppUrl in homeSubCatAppUrls:
                print 'Subcat url', HOME_URL + homeSubCatAppUrl
                homeAppDetail = home_app_detail(HOME_URL + homeSubCatAppUrl)
                homeApp = models.HomeApp(**homeAppDetail)
                homeApp.save()
                homeSubCatObject.apps.add(homeApp)
                
        
        home_app_urls = []
        for home_collection_name in home_collections:
            home_subcollections = home_collections[home_collection_name]
            home_collection_object = models.HomeCollection.objects.create(name=home_collection_name)

            for home_subcollection in home_subcollections:
                home_subcollection['collection'] = home_collection_object
                homeSubCollectionObject = models.HomeSubCollection.objects.create(**home_subcollection)

                subcollection_app_urls = getAllApps(HOME_URL + home_subcollection['url'])

                for subcollection_app_url in subcollection_app_urls:
                    subcollection_app_url = HOME_URL+ subcollection_app_url
                    print "Sub collection url", subcollection_app_url
                    homeAppDetail = home_app_detail(subcollection_app_url)
                    homeApp = models.HomeApp.objects.create(**homeAppDetail)
                    homeSubCollectionObject.apps.add(homeApp)

    if subcategories:
        print "DATA"
        #for each categories retrieve every sub categories 
        sub_categories = []
        sub_category_collections = {}
        print(categories)
        for index, category in enumerate(categories):
            full_url =  HOME_URL + category['url']
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
                
            counter = models.SubCategory.objects.count()+1
            for label, url in sub_categories_label:
                subcat = models.SubCategory(**{'category' : models.Category.objects.get(id=category['id']),  'id' : counter, 'name' : base64.b64encode(label), 'url' : url})
                subcat.save() 
                sub_categories.append({'id' : counter , 'category__id' : category['id'], 'name' : label, 'url' : url});
                counter+=1



    
    if not subcategories:
        sub_categories = [{'id' : subcat.id, 'category__id' : subcat.category.id, 'name' : subcat.name, 'url' : subcat.url } for subcat in models.SubCategory.objects.all()]
    #get apps in sub category 
    app_urls = set()


    if not appUrls:
        for app_url in models.AppUrl.objects.all():
            app_urls.add((app_url.category, app_url.url, app_url.subcategory))

    if appUrls:
        for sub_category in sub_categories:
            print sub_category['name']
            current_page = 0

            #to get full app list change language to english 
            sub_category_url = "https://cafebazaar.ir/" + sub_category['url'] + "?&p=" + str(current_page) + "&partial=true"
            params = {'l' : 'en'}
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
                    app_urls.add( ( sub_category['category__id'], (app.get('href')).encode('utf-8').strip(), sub_category['id'], sub_category['name'] ))
                    models.AppUrl.objects.create(**{ 'category' : sub_category['category__id'], 'url' : (app.get('href')).encode('utf-8').strip(), 'subcategory' : sub_category['id'] })
                sub_category_url = "https://cafebazaar.ir/" + sub_category['url'] + "?&p=" + str(current_page) + "&partial=true"
                html = requests.get(sub_category_url)
                soup = BeautifulSoup(html.text, 'lxml')
                apps = soup.select(".msht-app-list a")
            print len(app_urls)

   
    
    #retrieve app detail 
    if appDetail:
        app_details = []
        counter = 0
        for app_url_ in app_urls:
            print counter, app_url
            app_url_en = HOME_URL + app_url_[1]

            #change app to iran lanuage so to get information in iran lanuage
            params = {'l' : 'fa'}
            app_url = ""
            url_parts = list(urlparse.urlparse(app_url_en))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update(params)
            url_parts[4] = urlencode(query)
            app_url= urlparse.urlunparse(url_parts)
            counter+=1
            html = requests.get(app_url)
            soup = BeautifulSoup(html.text, 'lxml')
            
            html_en = requests.get(app_url_en)
            soup_en = BeautifulSoup(html_en.text, 'lxml')
            
            icon_sel = ".app-img"
            title_sel = ".app-name h1"
            dev_sel = ".dev a"
            price_sel = ".price a"
            screen_shots = ".screenshot-holder .screenshot-wrp a"
            description_sel = ".container .row.margin-top-sm" #6th element 
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
                app_detail['developer'] = (soup.select(dev_sel)[0].get_text()).encode('utf-8').strip()
                app_detail['developer_url'] = soup.select(dev_sel)[0].get('href')
                app_detail['price'] =(soup.select(price_sel)[0].get_text()).encode('utf-8').strip()
                screenshots = ["https:" + screenshot.get('href') for screenshot in soup.select(screen_shots)]
                app_detail['cateogry'] = models.Category.objects.get(id=app_url_[0])
                app_detail['sub_category'] = models.SubCategory.objects.get(id=app_url_[2])
                app_detail['rating_total'] = soup_en.select(rating_total)[0].get_text().encode('utf-8').strip()
                app_detail['rating_total_count'] = soup_en.select(rating_total_count)[0].get_text().encode('utf-8').strip()
                app_detail['url'] = app_url
                app_detail['package_name'] = app_url.split("/")[-2]
            except Exception as e :
                print e
                continue

            try:
                app_description = (soup.select(description_sel)[0].findNext('div').find('.col-sm-8').get_text()).encode('utf-8').strip()
                print app_description;
            except:
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
            
            app = models.App(**app_detail)
            app.save()
            
            for screenshoturl in screenshots:
                models.Screenshot(app = app, url=screenshoturl).save()
            app_details.append(app_detail)
    
    return 'Done'
#import json
#print(json.dumps( app_details ))


        

