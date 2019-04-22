import requests
from bs4 import BeautifulSoup
import models
import base64

def scrap():
    PAGE_INC = 24
    categories_url = "https://cafebazaar.ir/cat/?partial=true"
    html = requests.get(categories_url)

    soup = BeautifulSoup(html.text, 'lxml')

    #get list of app categories 
    # all_apps_ul = soup.find('ul')
    # all_apps = all_apps_ul.find_all('a')
    # app_categories = []
    # for index, app in enumerate(all_apps):
    #     app_categories.append({'id' : index, 'text' :app.get_text().encode('utf-8').strip(), 'url' : (app.get('href')).strip() }) 
    #     category = models.Category(**{'id' : index, 'category_type' : 1, 'name' :app.get_text().encode('utf-8').strip(), 'url' : (app.get('href')).strip() })
    #     category.save()        
    
    # #get list of game cateogries
    # all_games_ul = soup.find_all('ul')[1]
    # all_games = all_games_ul.find_all('a')
    # game_categories = []
    # for index, game in enumerate(all_games):
    #     game_categories.append({'id' : index+24, 'text' : (game.get_text()).encode('utf-8').strip(), 'url' : (game.get('href')).strip() }) 
    #     models.Category.objects.create(**{'id' : index+24,'category_type' : 2, 'name' : (game.get_text()).encode('utf-8').strip(), 'url' : (game.get('href')).strip() })
        
    categories = [ {'id' : category.id, 'text' : category.name, 'category_type' : category.category_type, 'url' : category.url } for category in  models.Category.objects.all()]
    #categories = app_categories + game_categories
    sub_category_selector = ".msht-row-head .msht-row-title"
    sub_category_link_sel = ".msht-row-more a"

    #for each categories retrieve every sub categories 
    # sub_categories = []
    # for index, category in enumerate(categories):
    #     full_url =  "https://cafebazaar.ir" + category['url']
    #     html = requests.get(full_url)
        
    #     soup = BeautifulSoup(html.text, 'lxml')
    
    #     sub_categories_label = [(sub_category_selected.get_text()).encode('utf-8').strip() for sub_category_selected in soup.select(sub_category_selector)]
        
    #     sub_categories_url = [(sub_category_link_selected.get('href')).encode('utf-8').strip() for sub_category_link_selected in soup.select(sub_category_link_sel)]
        
        
    #     counter = models.SubCategory.objects.count()
    #     for label, url in zip(sub_categories_label, sub_categories_url):
    #         subcat = models.SubCategory(**{'category' : models.Category.objects.get(id=category['id']),  'id' : counter, 'name' : base64.b64encode(label), 'url' : url})
    #         subcat.save() 
    #         sub_categories.append({'id' : counter , 'category__id' : category['id'], 'name' : label, 'url' : url});
    #         counter+=1
        
    sub_categories = [{'id' : subcat.id, 'category__id' : subcat.category.id, 'name' : subcat.name, 'url' : subcat.url } for subcat in models.SubCategory.objects.all()]
    current_page = 0
    #get apps in sub category 
    app_urls = set()
    for app_url in models.AppUrl.objects.all():
        app_urls.add((app_url.category, app_url.url, app_url.subcategory))
    # for sub_category in sub_categories:
    #     sub_category_url = "https://cafebazaar.ir/" + sub_category['url'] + "?l=en&p=" + str(current_page) + "&partial=true"
    #     html = requests.get(sub_category_url)
    #     soup = BeautifulSoup(html.text, 'lxml')
    #     while soup.find("meta"):
    #         current_page += PAGE_INC
    #         html = requests.get(sub_category_url)
    #         soup = BeautifulSoup(html.text, 'lxml')
    #         apps = soup.select(".msht-app-list a")

    #         for app in apps:
    #             app_urls.add( ( sub_category['category__id'], (app.get('href')).encode('utf-8').strip(), sub_category['id'] ))
    #             models.AppUrl.objects.create(**{ 'category' : sub_category['category__id'], 'url' : (app.get('href')).encode('utf-8').strip(), 'subcategory' : sub_category['id'] })
    #         sub_category_url = "https://cafebazaar.ir/" + sub_category['url'] + "?l=en&p=" + str(current_page) + "&partial=true"
    #         html = requests.get(sub_category_url)
    #         soup = BeautifulSoup(html.text, 'lxml')
        
        
        
        


    #retrieve app detail 
    app_details = []
    counter = 0
    for app_url_ in app_urls:
        
        counter+=1
        app_url = "https://cafebazaar.ir" + app_url_[1]
        print counter, app_url
        html = requests.get(app_url)
        soup = BeautifulSoup(html.text, 'lxml')

        icon_sel = ".app-img"
        title_sel = ".app-name h1"
        dev_sel = ".dev a"
        price_sel = ".price a"
        screen_shots = ".screenshot-holder .screenshot-wrp a"
        description_sel = ".ltr p" #6th element 
        app_attributes = ".col-sm-4 div span"
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
            app_detail['url'] = app_url

        except:
            continue
        try:
            app_detail['description'] = (soup.select(description_sel)[6].get_text()).encode('utf-8').strip()
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
    
    return app_details
#import json
#print(json.dumps( app_details ))


        

