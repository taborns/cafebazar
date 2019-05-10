import requests
from bs4 import BeautifulSoup
from cafe import models
from scrapFuncs import *
# Importing all needed modules
from multiprocessing.pool import ThreadPool

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
        all_apps = []

        for rankRow in rankRows:
                app = {}
                if not rankRow.select('td.ranking-rank'):
                        continue

                app['rank'] = int(rankRow.select('td.ranking-rank')[0].get_text().strip())
                app['name'] = rankRow.select('td.ranking-app-cell a')[0].get_text()
                url = rankRow.select('td.ranking-app-cell a')[0].get('href')
                package_name = url.split('/')[-1]
                app['packagename'] = package_name

                app['developer'] = rankRow.select('.ranking-app-cell-creator a')[0].get_text()
                app['rating'] = rankRow.select('td.ranking-rating-cell span')[0].get_text().strip()
                app['category'] = rankRow.select('td.ranking-app-cell')[0].findNext('td').get_text().strip()
                app['installs'] = rankRow.select('td.ranking-rating-cell')[0].findNext('td').get_text().strip()
                app['rankfilter'] = filterData
                app['rankcat'] = catData
                rankApp = models.RankApp.objects.filter(packagename=app['packagename'], rankfilter=app['rankfilter'], rankcat=app['rankcat']).first()
                if rankApp:
                        app['icon'] = rankApp.icon
                else:
                        print "No app found", app['rankfilter'].pk, app['rankcat'].pk, app['packagename']
                        app['icon'] =  convertWebp(rankRow.select('td.ranking-icon-cell img')[0].get('data-src'))
                
                rankApp = models.RankApp(**app)
                all_apps.append(rankApp)

        return all_apps

        

# Define a function for the thread
def theScrapper( main_cat, app_filter):
        all_apps = saveApp(app_filter, main_cat)
        app_filter.apps.filter(rankcat=main_cat).delete()
        for app in all_apps:
                app.save()
        print "DONE", app_filter.pk, main_cat.pk, app_filter.apps.filter(rankcat=main_cat).count();


def rankScrap():
        app_filters = models.RankFilter.objects.all()
        main_cats = models.RankCat.objects.all()
        thread_count = 10 
        thread_pool = ThreadPool(processes=thread_count) 
        known_threads = {}

        for main_cat in main_cats:
                for app_filter in app_filters:
                        thread_pool.apply_async(theScrapper, args=(main_cat,app_filter))

        thread_pool.close() # After all threads started we close the pool
        thread_pool.join() # And wait until all threads are done


        return "DONE"








    

        
    
    