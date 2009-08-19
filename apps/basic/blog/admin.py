from django.contrib import admin
from basic.blog.models import *
from basic.blog.forms import PostAdminForm
from django import forms
from utils import trunc
from twitterapp.utils import UpdateStatusFromLocalLink


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


def SavePost(post, sendTweet):
    post.save()
    if sendTweet:
        try:
            description = post.tease
            if len(post.tease)==0:
                description = post.title
            
            UpdateStatusFromLocalLink(description, post.get_absolute_url())
            
        except Exception, e:
            pass

    
class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status',)
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    
    def save_model(self, request, obj, form, change):
        SavePost(obj, form.cleaned_data['twitter'])

admin.site.register(Post, PostAdmin)