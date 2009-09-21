'''
Created on 13 Aug 2009

@author: dalore
'''

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from basic.blog import views as blog_views

urlpatterns = patterns('',
    # home page
    url(r'^$', direct_to_template, {'template':'index.html'}, name='home'),
    
    url(r'^about.html$', direct_to_template, {'template':'about.html'}, name='about'),
    url(r'^people.html$', direct_to_template, {'template':'people.html'}, name='people'),
    url(r'^services.html$', direct_to_template, {'template':'services.html'}, name='services'),
    url(r'^clients.html$', direct_to_template, {'template':'clients.html'}, name='clients'),
    url(r'^labs/$', blog_views.labs_list, {'template_name':'blog/labs_list.html'}, name='labs'),
    url(r'^blog/$', direct_to_template, {'template':'blog/'}, name='blog'),
    url(r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}, name='robotstxt'),
)