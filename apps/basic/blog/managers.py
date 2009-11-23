from django.db.models import Manager
import datetime


class PublicManager(Manager):
    """Returns published posts that are not in the future."""
    
    def published(self, user=None):
        query = self.get_query_set().filter(publish__lte=datetime.datetime.now())
        if user and not user.is_staff:
            query = query.filter(status__gte=2)
        return query