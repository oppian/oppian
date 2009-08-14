from django.contrib import admin
from basic.blog.models import *
from basic.blog.forms import PostAdminForm
from django import forms
from utils import trunc
from twitterapp.utils import UpdateStatusFromLocalLink


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


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
                description = obj.tease
                if len(obj.tease)==0:
                    description = obj.title
                
                UpdateStatusFromLocalLink(description, obj.get_absolute_url())
                
            except Exception, e:
                pass

admin.site.register(Post, PostAdmin)