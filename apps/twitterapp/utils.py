from django.contrib.sites.models import Site
from django.conf import settings
from twitter.api import Twitter, TwitterError
from url_shortener.models import Link

    
def UpdateStatusFromLocalLink(description, local_url, format_str=u"'%(description)s' - %(url)s"):
    current_site = Site.objects.get_current()
    url = "http://%s%s" %(current_site, local_url)
    
    link = None
    try:
        link = Link.objects.get(url=url)
    except:
        pass
    if not link:
        link = Link.objects.create(url=url)    
    short_url = link.short_url()

    shortest_status = format_str % {'description': "", "url": ""}
    
    max_len = 140-len(short_url)-len(shortest_status)
    
    if len(description)>max_len:
        description = trunc(description, max_pos=max_len)
    
    UpdateStatus(format_str % {'description': description, "url": short_url})
    

def UpdateStatus(status):
    twitter = Twitter(settings.TWITTER_EMAIL, settings.TWITTER_PASSWORD, agent=settings.TWITTER_AGENT_STR)
    status_utf8= status.encode('utf8', 'replace')
    twitter.statuses.update(status=status_utf8)