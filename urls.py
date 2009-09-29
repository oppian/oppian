from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from basic.blog.feeds import BlogPostsFeed, BlogPostsByCategory

feeds = {
    'latest': BlogPostsByCategory,
}


urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # contact form
    (r'^contact/', include('contact_form.urls')),
    
    # blog
    (r'^blog/', include('basic.blog.urls')),
    
    # link shortener
    (r'^o/', include('url_shortener.urls')),
    
    # robot crontrol
    (r'^robots.txt$', include('robots.urls')),
    
    # feeds
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
        
    # last, the about pages and home page etc
    (r'^', include('oppianapp.urls')),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        # static files, note: use of settings for DRY
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^(?P<path>favicon.ico)$', 'django.views.static.serve', {
            'document_root': '%s/images/' % settings.MEDIA_ROOT,
        }),
    )

handler500 = 'oppianapp.views.server_error'

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', handler500),
    )