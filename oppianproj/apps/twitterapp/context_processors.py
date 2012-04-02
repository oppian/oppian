from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from twitter.api import Twitter
import sys

def latest_tweet(request):
    tweet = cache.get('tweet')

    if not tweet:
        try:
            twitter = Twitter(settings.TWITTER_EMAIL, settings.TWITTER_PASSWORD, agent=settings.TWITTER_AGENT_STR)
            tweet = twitter.statuses.friends_timeline(count=1)
            if tweet:
                tweet = tweet[0]
                tweet['date'] = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
                cache.set('tweet', tweet, settings.TWITTER_TIMEOUT)
        except:
            log = 'exception when reading the twitter friends timeline (for "%s") - %s' %(settings.TWITTER_EMAIL, sys.exc_info()[0])
            print >> sys.stderr, log
            sys.stderr.flush()
            pass

    return {"tweet": tweet}
