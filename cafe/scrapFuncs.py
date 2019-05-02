import requests
from bs4 import BeautifulSoup
import base64
import urlparse
from urllib import urlencode
from PIL import Image
from django.conf import settings


PAGE_INC = 24
HOME_CAT_ID = -10
IMAGE_PATH = settings.MEDIA_ROOT

def convertWebp(url, size=(100,100), prefix='icon-'):
    import random
    randnum = random.randint(1000,10000)

    image_name = url.split('/')[-1].rsplit('.', 1)[0]
    image_name = prefix + image_name + str(randnum) + '.webp'
    image = Image.open(requests.get(url, stream=True).raw)
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(IMAGE_PATH + '/' + image_name, 'webp', optimize=True)

    return image_name



def buildUrl(url, current_page=0, lan='en'):
    app_url = url + "?&p=" + str(current_page) + "&partial=true"
    params = {'l' : lan}
    url_parts = list(urlparse.urlparse(app_url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    app_url= urlparse.urlunparse(url_parts)

    return app_url

#apps_url : FUll url 
def getAllApps(app_url_):
    current_page = 0
    home_app_urls = []
    #to get full app list change language to english 
    app_url = buildUrl(app_url_)

    html = requests.get(app_url)
    soup = BeautifulSoup(html.text, 'lxml')
    apps = soup.select(".msht-app-list a")
    while len(apps)>0:
        current_page += PAGE_INC

        for app in apps:
            home_app_urls.append( ( app.get('href')).encode('utf-8').strip() )
            #models.AppUrl.objects.create(**{ 'category' : home_subcollection['category__id'], 'url' : (app.get('href')).encode('utf-8').strip(), 'subcategory' : home_subcollection['id'] })
        app_url = buildUrl(app_url_, current_page)
        html = requests.get(app_url)
        soup = BeautifulSoup(html.text, 'lxml')
        apps = soup.select(".msht-app-list a")
    
    return home_app_urls
def home_app_detail(app_url_):
    app_url_en = app_url_
    #change app to iran lanuage so to get information in iran lanuage
    params = {'l' : 'fa'}
    app_url = ""
    url_parts = list(urlparse.urlparse(app_url_en))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    app_url= urlparse.urlunparse(url_parts)
    html = requests.get(app_url)
    soup = BeautifulSoup(html.text, 'lxml')
    
    html_en = requests.get(app_url_en)
    soup_en = BeautifulSoup(html_en.text, 'lxml')
    
    icon_sel = ".app-img"
    title_sel = ".app-name h1"
    dev_sel = ".dev a"
    price_sel = ".price a"
    screen_shots = ".screenshot-holder .screenshot-wrp a"
    description_sel = ".ltr p" #6th element 
    app_attributes = ".col-sm-4 div span"
    rating_total = ".rating-total"
    rating_total_count = ".rating-total-count"
    categoryID = 6
    installsID = 9
    sizeID = 11
    versionID = 13
    app_detail = {}
    try:
        app_detail['icon'] = convertWebp("https:" + soup.select(icon_sel)[0].get('src'))
        app_detail['name'] = (soup.select(title_sel)[0].get_text()).encode('utf-8').strip()
        app_detail['price'] =(soup.select(price_sel)[0].get_text()).encode('utf-8').strip()
        app_detail['rating_total'] = soup_en.select(rating_total)[0].get_text().encode('utf-8').strip()
        app_detail['rating_total_count'] = soup_en.select(rating_total_count)[0].get_text().encode('utf-8').strip()
        app_detail['url'] = app_url
        app_detail['package_name'] = app_url.split("/")[-2]
    except Exception as e :
        print e
        return

    return app_detail

