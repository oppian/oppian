'''
Created on 14 August 2009

@author: steve
'''

from django.conf import settings
print settings.INSTALLED_APPS
from django.db.models import signals
from django.utils.translation import ugettext_noop as _
from django.contrib.contenttypes.models import ContentType

if "basic.inlines" in settings.INSTALLED_APPS:
    from basic.inlines import models as inlines
    from basic.media.models import Photo
    
    def create_inline_types(app, created_models, verbosity, **kwargs):
        print "creating inline types:"
        photo_content_type = ContentType.objects.get_for_model(Photo)
        inline_type_photo = inlines.InlineType(title="Photo", content_type=photo_content_type)
        inline_type_photo.save()
        print "  photo"
        
    signals.post_syncdb.connect(create_inline_types, sender=inlines)
else:
    print "Skipping creation of InlineTypes as inline types app not found"