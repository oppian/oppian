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
    
    # fixed pages - first level
    url(r'^services/$', direct_to_template, {'template':'about/services.html'}, name='services'),
    url(r'^clients/$', direct_to_template, {'template':'about/clients.html'}, name='clients'),
    
    # fixed pages - about and sub about
    url(r'^about/$', direct_to_template, {'template':'about/about.html'}, name='about'),
    url(r'^about/people/$', direct_to_template, {'template':'about/people.html'}, name='about_people'),
    url(r'^about/jobs/$', direct_to_template, {'template':'about/jobs.html'}, name='about_jobs'),
    url(r'^about/contact_us/$', direct_to_template, {'template':'about/contact_us.html'}, name='about_contactus'),
)