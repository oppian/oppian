from django.conf import settings
from django import VERSION as DJANGO_VERSION
from django.conf import settings

class BuildMiddleware(object):

    def process_response(self, request, response):
        response['X-Django-Version'] = 'Django/%s.%s.%s.%s.%s' % DJANGO_VERSION
        key = 'X-%s-Version' % settings.BUILD_APPNAME
        response[key] = '%s-%s.%s' % (settings.BUILD_APPNAME, 
            settings.BUILD_VERSION[0], settings.BUILD_VERSION[1])
        return response
