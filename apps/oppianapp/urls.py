'''
Created on 13 Aug 2009

@author: dalore
'''

from django.conf.urls.defaults import *

# direct to template
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # home page
    url(r'^$', direct_to_template, {'template':'index.html'}, name='home'),
    
    url(r'^about.html$', direct_to_template, {'template':'about.html'}, name='about'),
    url(r'^people.html$', direct_to_template, {'template':'people.html'}, name='people'),
    url(r'^services.html$', direct_to_template, {'template':'services.html'}, name='services'),
    url(r'^clients.html$', direct_to_template, {'template':'clients.html'}, name='clients'),
    url(r'^labs.html$', direct_to_template, {'template':'labs.html'}, name='labs'),
    url(r'^blog.html$', direct_to_template, {'template':'blog.html'}, name='blog'),
    url(r'^contact.html$', direct_to_template, {'template':'contact.html'}, name='contact'),
    url(r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}, name='robotstxt'),
)