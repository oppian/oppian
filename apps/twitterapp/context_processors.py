from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from twitter.api import Twitter, TwitterError

 
def latest_tweet(request):
    tweet = cache.get('tweet')

    if tweet:
        return {"tweet": tweet}

    try:
        twitter = Twitter(settings.TWITTER_EMAIL, settings.TWITTER_PASSWORD, agent=settings.TWITTER_AGENT_STR)
        tweet = twitter.statuses.friends_timeline(count=1)[0]
        tweet['date'] = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        cache.set('tweet', tweet, settings.TWITTER_TIMEOUT)
    except TwitterError, e:
        pass
    

    return {"tweet": tweet}
