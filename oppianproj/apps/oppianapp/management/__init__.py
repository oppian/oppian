'''
Created on 14 August 2009

@author: steve
'''

from django.conf import settings
print settings.INSTALLED_APPS
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify


"""
Creates the default oppian data.
"""


"""
Creates the default media - photos.
"""
if "basic.media" in settings.INSTALLED_APPS:
    from basic.inlines import models as media
    from basic.media.models import Photo
    import os, glob

    
    def create_photo(path, leafname, verbosity):
        filename = '%s%s' % (path, leafname)
        photos = Photo.objects.filter(photo=filename)
        if len(photos)==0:
            title = leafname
            description = leafname
            photo = Photo(
                        title=title, 
                        slug=slugify(title), 
                        photo=filename,
                        license="http://creativecommons.org/licenses/by-nc-nd/2.0/",
                        description=description, 
                        tags="logo, oppian")
            photo.save()
            if verbosity >= 2:
                print '  Adding "%s""' % filename
        
    def create_initial_media(app, created_models, verbosity, **kwargs):
        if verbosity >= 2:
            print "creating initial media:"
            
        images_dir = '%s/images' % settings.MEDIA_ROOT_LOCAL
        os.chdir(images_dir)

        # currently only get PNG and JPEG files
        filenames = glob.glob("*.png") + glob.glob("*.jpg")
        for filename in filenames:
            create_photo('images/', filename, verbosity)

    signals.post_syncdb.connect(create_initial_media, sender=media)
else:
    print "Skipping creation of initial inline photos as inline app not found"


"""
Creates the default Site object.
"""
from django.contrib.sites.models import Site
from django.contrib.sites import models as site_app

def create_default_site(app, created_models, verbosity, **kwargs):
    if Site in created_models:
        # first check for existing site id
        try:
            site = Site.objects.get(id=settings.SITE_ID)
            # delete it if it exists
            site.delete()
        except:
            # site doesn't exist
            pass

        if verbosity >= 2:
            print " Site object"
        s = Site(id=settings.SITE_ID, domain=settings.SITE_DOMAIN, name=settings.SITE_NAME)
        s.save()
    Site.objects.clear_cache()

signals.post_syncdb.connect(create_default_site, sender=site_app)
