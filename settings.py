# Django settings for oppian project.

import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = True

ADMINS = (
    ('Matthew Jacobi', 'matt@oppian.com'),
    ('Steve Hartley', 'steve@oppian.com'),
    ('Lighthouse', 'ticket+oppian.24019-zcj7zsja@lighthouseapp.com'),
)

MANAGERS = ADMINS

# only serve media in Django in debug mode as in release mode, it is served by Apache
SERVE_MEDIA = DEBUG

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_ROOT, '.sqlite.db')              # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1
SITE_NAME = 'Oppian'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# if SHORTENER_REQUIRES_LOGIN is True, then only logged in users can submit new URLs
SHORTENER_REQUIRES_LOGIN = True

# add the template context processor for the latest tweet
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    "twitterapp.context_processors.latest_tweet",
    "oppianapp.context_processors.settings",
)

# the twitter email account of the site 
TWITTER_EMAIL = "twitter-test@oppian.com"
#TWITTER_EMAIL = "twitter@oppian.com"
# the password for the account referenced by the twitter email address above
TWITTER_PASSWORD = "metef62" # oppian-test
#TWITTER_PASSWORD = "deteenee52" # oppian
# the name of the agent making the requests
TWITTER_AGENT_STR = "www.oppian.com"
# how often to check the tweet status
TWITTER_TIMEOUT = 3600

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/m/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4tt(s*od&lp(6wrd#iwq=vmot%#9nfl%00k=q5$eplz3lkgr0z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'build.middleware.BuildMiddleware', # insert build version into headers
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "templates").replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.humanize',
    
    # basic apps http://github.com/nathanborror/django-basic-apps/tree/master
    'basic.*',
    
    # url shortener git://github.com/nileshk/url-shortener.git 
    'url_shortener',
    
    # tagging http://code.google.com/p/django-tagging/
    'tagging',
    
    # django command extensions http://github.com/django-extensions
    'django_extensions',
    
    # about (static pages)
    'about',
    
    # build tools
    'build',
    
    # oppian web-site specific code
    'oppianapp',
)

# AWS
AWS_ACCESS_KEY_ID = '1EZPW78HVZMFXZXJXAR2'
AWS_SECRET_ACCESS_KEY = 'ZXslmLM93TYrGA33GFyzIozSSN4VH1wrNXzyjXIt'

# build
AWS_BUILD_BUCKET_NAME = 'oppian-website-releases'
BUILD_VERSION = ('0', '2')
BUILD_APPNAME = 'oppian'

# email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'www@oppian.com'
EMAIL_HOST_PASSWORD = '4E6993'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# default from address for errors
import socket
SERVER_EMAIL = '"%s" <www@oppian.com>' % socket.gethostname()
# default from address for normal email
DEFAULT_FROM_EMAIL = 'www@oppian.com'


# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from settings_local import *
except ImportError:
    try: 
        # no settings_local, then use settings_production
        from settings_production import *
    except ImportError:
        pass
