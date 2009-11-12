from django.conf import settings
from django import http
from django.template import Context, loader, RequestContext
from models import LabsPost
from django.shortcuts import render_to_response
from basic.blog.models import *
from django.views.generic import date_based, list_detail
from django.core.urlresolvers import reverse

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))
    
def _get_menu(posts=None, user=None):
    if not posts:
        posts = LabsPost.objects.published(user)
    menu = []
    menu.append({
        'name': 'Oppian Labs',
        'url': reverse('labs')
    })
    for post in posts:
        menu.append({
            'name': post.title,
            'url': post.get_absolute_url()
        })
    return menu
    

def labs_list(request, template_name = 'blog/labs_list.html', page=0, **kwargs):
    """
    Returns a list of labs posts.
    """
    # filter for lab category
    labsposts = LabsPost.objects.published(request.user).filter(categories__slug='lab')

    return list_detail.object_list(
        request,
        queryset = labsposts,
        template_name = template_name,
        paginate_by = 10,
        page = page,
        extra_context = {'menu':_get_menu(labsposts)},
        **kwargs
    )

def labs_detail(request, slug):
    post = LabsPost.objects.get(slug=slug)
    return render_to_response('blog/lab_detail.html',{
        'object': post,
    }, context_instance=RequestContext(request))
