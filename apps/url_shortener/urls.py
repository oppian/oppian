from django.conf.urls.defaults import *
from views import index, submit, follow, info

urlpatterns = patterns('',
    url(r'^$', index, name="shortener_index"),
    url(r'^submit/$', submit, name="shortener_submit"),
    url(r'^(?P<base62_id>\w+)$', follow, name="shortener_follow"),
    url(r'^info/(?P<base62_id>\w+)$', info, name="shortener_info"),
)
