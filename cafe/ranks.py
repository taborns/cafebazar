import requests
from bs4 import BeautifulSoup
from cafe import models
from scrapFuncs import *


HOME_URL = 'https://www.appbrain.com'
main_cats = {'top_new_free' : '/stats/google-play-rankings/top_new_free/all/ir', 'top_free' : '/stats/google-play-rankings/top_free/all/ir', 'top_grossing' : '/stats/google-play-rankings/top_grossing/all/ir'}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3683.103 Safari/537.36'}


def saveCats():
    for main_cat_key in main_cats:
        models.RankCat.objects.create(catcode= main_cat_key, name=main_cat_key.replace('_', ' ').title())

#get all filters for each main categories
def saveAppFilters():

    main_cat = models.RankCat.objects.first()
    app_list_url = HOME_URL + '/stats/google-play-rankings/' + main_cat.catcode + '/all/ir'
    print app_list_url
    html = requests.get(app_list_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')

    select_items = soup.select('#category_popup a.item')
    for select_item in select_items:
        filter_url = select_item.get('href').strip()
        filtercode = filter_url.split('/')[-2]

        filter_data = {'name' : select_item.get_text().strip() , 'filtercode' : filtercode}
        models.RankFilter.objects.create(**filter_data)
    


def saveApp(filterData, catData):
    
    app_list_url = HOME_URL + '/stats/google-play-rankings/' + catData.catcode + '/' + filterData.filtercode+ '/ir'
    html = requests.get(app_list_url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    
    rankRows = soup.select('#rankings-table tbody tr')

    top_apps = []
    for rankRow in rankRows:
        app = {}
        if not rankRow.select('td.ranking-rank'):
            continue

        app['rank'] = int(rankRow.select('td.ranking-rank')[0].get_text().strip())
        app['name'] = rankRow.select('td.ranking-app-cell a')[0].get_text()
        url = rankRow.select('td.ranking-app-cell a')[0].get('href')
        package_name = url.split('/')[-1]
        app['packagename'] = package_name
        
        app['icon'] =  convertWebp(rankRow.select('td.ranking-icon-cell img')[0].get('data-src'))
        app['developer'] = rankRow.select('.ranking-app-cell-creator a')[0].get_text()
        app['rating'] = rankRow.select('td.ranking-rating-cell span')[0].get_text().strip()
        app['category'] = rankRow.select('td.ranking-app-cell')[0].findNext('td').get_text().strip()
        app['installs'] = rankRow.select('td.ranking-rating-cell')[0].findNext('td').get_text().strip()
        app['rankfilter'] = filterData
        app['rankcat'] = catData
        models.RankApp.objects.create(**app)

def rankScrap():
    app_filters = models.RankFilter.objects.all()
    main_cats = models.RankCat.objects.all()
    all_list = {}

    for main_cat in main_cats:
        print "Category", main_cat.name 
        for app_filter in app_filters:
            print "Filter", app_filter.name
            saveApp(app_filter, main_cat)



    

        
    
    