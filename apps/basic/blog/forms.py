from basic.blog.models import Post
from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js', 
        )

    twitter = forms.BooleanField(required=False, label="Post link to Twitter", initial=True)
