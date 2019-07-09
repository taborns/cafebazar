from cafe.models import *

def doTheDirtyWork():
    app_urls =  AppUrl.objects.all()
    counter = 0
    main_counter = 0
    for app_url in app_urls:
        try:
            #print "https://cafebazaar.ir" + app_url.url
            app = App.objects.get(url="https://cafebazaar.ir" + app_url.url)
            app.cateogry = app_url.category
            app.sub_category = app_url.subcategory
            app.save()
            main_counter +=1
        except Exception as e:
            #print e
            print e, counter+1, main_counter
            counter += 1
            continue