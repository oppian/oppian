import datetime

from django.db import models
from django.conf import settings
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings

#from urlweb.shortener.baseconv import base62
from baseconv import base62

class Link(models.Model):
    """
    Model that represents a shortened URL

    # Initialize by deleting all Link objects
    >>> Link.objects.all().delete()
    
    # Create some Link objects
    >>> link1 = Link.objects.create(url="http://www.google.com/")
    >>> link2 = Link.objects.create(url="http://www.nileshk.com/")

    # Get base 62 representation of id
    >>> link1.to_base62()
    'B'
    >>> link2.to_base62()
    'C'
    
    # Get short URL's
    >>> link1.short_url()
    'http://uu4.us/B'
    >>> link2.short_url()
    'http://uu4.us/C'

    # Test usage_count
    >>> link1.usage_count
    0
    >>> link1.usage_count += 1
    >>> link1.usage_count
    1

    """
    url = models.URLField(verify_exists=True, unique=True)
    date_submitted = models.DateTimeField(default=datetime.datetime.now())
    usage_count = models.IntegerField(default=0)

    def to_base62(self):
        return base62.from_decimal(self.id)

    def short_url(self):
        current_site = Site.objects.get_current()
        url=reverse('shortener_follow', args=[self.to_base62()])
        return 'http://%s%s' %(current_site.domain, url)

    def __unicode__(self):
        return self.to_base62() + ' : ' + self.url

class LinkSubmitForm(forms.Form):
    u = forms.URLField(verify_exists=not settings.DEBUG,
                       label='URL to be shortened:',
                       )
