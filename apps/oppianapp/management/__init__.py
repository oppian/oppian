'''
Created on 14 August 2009

@author: steve
'''

from django.conf import settings
print settings.INSTALLED_APPS
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from django.contrib.contenttypes.models import ContentType

"""
Creates the default inline types - photo
"""
if "basic.inlines" in settings.INSTALLED_APPS:
    from basic.inlines import models as inlines
    from basic.media.models import Photo
    
    def create_inline_types(app, created_models, verbosity, **kwargs):
        print "creating inline types:"
        
        photo_content_type = ContentType.objects.get_for_model(Photo)
        types = inlines.InlineType.objects.filter(content_type=photo_content_type)
        if len(types)==0:
            inline_type_photo = inlines.InlineType(title="Photo", content_type=photo_content_type)
            inline_type_photo.save()
            print "  Adding photo"
    
    signals.post_syncdb.connect(create_inline_types, sender=inlines)
else:
    print "Skipping creation of InlineTypes as inline types app not found"

"""
Creates the default media - photos.
"""
if "basic.media" in settings.INSTALLED_APPS:
    from basic.inlines import models as media
    from django.template.defaultfilters import slugify
    from basic.media.models import Photo
    
    def create_o_logo_media(width, height):
        filename = "images/OppianO-%(width)dx%(height)d.png" % {'width':width, 'height':height}
        photos = Photo.objects.filter(photo=filename)
        if len(photos)==0:
            title = "Oppan-O Logo (%(width)d,%(height)d)" % {'width':width, 'height':height}
            description = "Oppian O logo with transparent background sized at %(width)d,%(height)d." % {'width':width, 'height':height}
            photo = Photo(
                        title=title, 
                        slug=slugify(title), 
                        photo=filename,
                        license="http://creativecommons.org/licenses/by-nc-nd/2.0/",
                        description=description, 
                        tags="logo, oppian")
            photo.save()
            print '  Adding "%s" - "%s"' % (filename, description)
        
    def create_initial_media(app, created_models, verbosity, **kwargs):
        print "creating initial media:"
        # to do - scan for files (in a directory?) under media
        create_o_logo_media(96,82)

    signals.post_syncdb.connect(create_initial_media, sender=media)
else:
    print "Skipping creation of initial inline photos as inline app not found"

"""
Creates the default blogs.
"""
if "basic.blog" in settings.INSTALLED_APPS:
    from basic.blog import models as blog
    from django.template.defaultfilters import slugify

    def create_initial_blogs(app, created_models, verbosity, **kwargs):
        print "creating initial blogs:"
        title = "Welcome to Oppian.com"
        blogs = blog.Post.objects.filter(title=title)
        if len(blogs)==0:
            post=blog.Post(
                title=title,
                body='<inline type="media.photo" id="1" class="small_left" />\nHello',
                tease=title,
                slug=slugify(title),
                status=2, # public
                allow_comments=True,
                publish="2009-01-01 00:00",
                created="2009-01-01 00:00")
            post.save()
            print '  Adding "%s"' % title
        
        
    signals.post_syncdb.connect(create_initial_blogs, sender=blog)
else:
    print "Skipping creation of initial blogs as blog app not found"


"""
Creates the default Site object.
"""
from django.contrib.sites.models import Site
from django.contrib.sites import models as site_app
import socket

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
        s = Site(id=settings.SITE_ID, domain=socket.gethostname(), name=settings.SITE_NAME)
        s.save()
    Site.objects.clear_cache()

signals.post_syncdb.connect(create_default_site, sender=site_app)