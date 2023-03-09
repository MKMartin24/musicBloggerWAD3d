import os
os.environ.setdefault('DJANGO_SSETTINGSMODULE','musicBloggerWAD3d.settings')

import django
django.setup
from rango.models import Category, Page

def populate():
    
    #python_pages = [
    #]

    #django_pages = [
    #]

    #other_pages = [
    #]

    #cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            #'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            #'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}
            #}

    
    #for cat, cat_data in cats.items():
        #c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        #for p in cat_data['pages']:
            #add_page(c, p['title'], p['url'], views=p['views'])

    #for c in Category.objects.all():
        #for p in Page.objects.filter(category=c):
            #print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start excution here
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()