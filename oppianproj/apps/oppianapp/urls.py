from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from basic.blog import views as blog_views
from views import *

urlpatterns = patterns('',
    # home page
    url(r'^$', direct_to_template, {'template':'index.html'}, name='home'),
    
    url(r'^about/$', direct_to_template, {'template':'about.html'}, name='about'),
    url(r'^people/$', direct_to_template, {'template':'people.html'}, name='people'),
    url(r'^services/$', direct_to_template, {'template':'services.html'}, name='services'),
    url(r'^recommended/$', direct_to_template, {'template':'recommended.html'}, name='recommended'),
    url(r'^clients/$', direct_to_template, {'template':'clients.html'}, name='clients'),
    url(r'^partners/$', direct_to_template, {'template':'partners.html'}, name='partners'),
    url(r'^blog/$', direct_to_template, {'template':'blog/'}, name='blog'),
    url(r'^map/$', direct_to_template, {'template':'map.html'}, name='map'),
    
    url(r'^robots.txt$', direct_to_template, {'template':'robots.txt', 'mimetype':'text/plain'}, name='robotstxt'),
    url(r'^mu-eb1fb975-6fa67f08-d4888dcd-0461d515/$', direct_to_template, {'template':'blitzio.txt', 'mimetype':'text/plain'}, name='blitzio'),
    
    # labs post
    url(r'^labs/$', labs_list, name='labs'),
    url(r'^labs/(?P<slug>[\w-]+)/$', labs_detail, name='labs-detail'),
)