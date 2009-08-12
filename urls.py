from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# settings for static files
from django.conf import settings

# direct to template
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # flat pages
    url(r'^$', direct_to_template, {'template':'index.html'}, name='home'),
    url(r'^services/$', direct_to_template, {'template':'services.html'}, name='services'),
    url(r'^about/$', direct_to_template, {'template':'about.html'}, name='about'),
    url(r'^clients/$', direct_to_template, {'template':'clients.html'}, name='clients'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # blog
    (r'^blog/', include('basic.blog.urls')),
    
    # link shortener
    (r'^o/', include('url_shortener.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # static files, note: use of settings for DRY
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^(?P<path>favicon.ico)$', 'django.views.static.serve', {
            'document_root': '%s/images/' % settings.MEDIA_ROOT,
        }),
    )
    