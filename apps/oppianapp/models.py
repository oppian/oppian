from basic.blog import models as blog
from django.db import models

class LabsPost(blog.Post):
    """
    Proxy model to handle lab posts.
    """
    class Meta:
        proxy = True
        
    @models.permalink
    def get_absolute_url(self):
        return ('labs-detail', None, {
            'slug': self.slug
        })