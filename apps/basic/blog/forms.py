from basic.blog.models import Post
from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post

    twitter = forms.BooleanField(required=False, label="Post link to Twitter", initial=True)
