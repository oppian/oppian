from django.contrib import admin
from basic.blog.models import *
from basic.blog.forms import PostAdminForm
from django import forms
from django.conf import settings
from django.contrib.sites.models import Site


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


"""Truncation beautifier function
This simple function attempts to intelligently truncate a given string
"""
__author__ = 'Kelvin Wong <www.kelvinwong.ca>'
__date__ = '2007-06-22'
__version__ = '0.10'
__license__ = 'LGPL v.2.1 http://www.gnu.org/licenses/lgpl.html'

def trunc(s,min_pos=0,max_pos=75,ellipsis=True):
    """Return a nicely shortened string if over a set upper limit 
    (default 75 characters)
    
    What is nicely shortened? Consider this line from Orwell's 1984...
    0---------1---------2---------3---------4---------5---------6---------7---->
    When we are omnipotent we shall have no more need of science. There will be
    
    If the limit is set to 70, a hard truncation would result in...
    When we are omnipotent we shall have no more need of science. There wi...
    
    Truncating to the nearest space might be better...
    When we are omnipotent we shall have no more need of science. There...
    
    The best truncation would be...
    When we are omnipotent we shall have no more need of science...
    
    Therefore, the returned string will be, in priority...
    
    1. If the string is less than the limit, just return the whole string
    2. If the string has a period, return the string from zero to the first
        period from the right
    3. If the string has no period, return the string from zero to the first
        space
    4. If there is no space or period in the range return a hard truncation
    
    In all cases, the string returned will have ellipsis appended unless
    otherwise specified.
    
    Parameters:
        s = string to be truncated as a String
        min_pos = minimum character index to return as Integer (returned
                  string will be at least this long - default 0)
        max_pos = maximum character index to return as Integer (returned
                  string will be at most this long - default 75)
        ellipsis = returned string will have an ellipsis appended to it
                   before it is returned if this is set as Boolean 
                   (default is True)
    Returns:
        Truncated String
    Throws:
        ValueError exception if min_pos > max_pos, indicating improper 
        configuration
    Usage:
    short_string = trunc(some_long_string)
    or
    shorter_string = trunc(some_long_string,max_pos=15,ellipsis=False)
    """
    # Sentinel value -1 returned by String function rfind
    NOT_FOUND = -1
    # Error message for max smaller than min positional error
    ERR_MAXMIN = 'Minimum position cannot be greater than maximum position'
    
    # If the minimum position value is greater than max, throw an exception
    if max_pos < min_pos:
        raise ValueError(ERR_MAXMIN)
    # Change the ellipsis characters here if you want a true ellipsis
    if ellipsis:
        suffix = '...'
    else:
        suffix = ''
    # Case 1: Return string if it is shorter (or equal to) than the limit
    length = len(s)
    if length <= max_pos:
        return s + suffix
    else:
        # Case 2: Return it to nearest period if possible
        try:
            end = s.rindex('.',min_pos,max_pos)
        except ValueError:
            # Case 3: Return string to nearest space
            end = s.rfind(' ',min_pos,max_pos)
            if end == NOT_FOUND:
                end = max_pos
        return s[0:end] + suffix



class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status',)
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if form.cleaned_data['twitter']:
            try:
                from twitter.api import Twitter, TwitterError
                twitter = Twitter(settings.TWITTER_EMAIL, settings.TWITTER_PASSWORD, agent=settings.TWITTER_AGENT_STR)
                current_site = Site.objects.get_current()
                url = "http://%s%s" %(current_site, obj.get_absolute_url())
                from url_shortener.models import Link
                link = Link.objects.get(url=url)
                if not link:
                    link = Link.objects.create(url=url)
                short_url = link.short_url()
                
                format_string = u"Blog: '%s' at %s"
                
                # a little shorter than the maximum as not taking account of the %s's
                max_len = 140-len(short_url)-len(format_string)
                description = obj.tease
                if len(obj.tease)>max_len:
                    description = trunc(obj.tease, max_pos=max_len)
                    
                statusTxt = format_string % (description, short_url)

                status = statusTxt.encode('utf8', 'replace')
                twitter.statuses.update(status=status)
            except Exception, e:
                pass

admin.site.register(Post, PostAdmin)