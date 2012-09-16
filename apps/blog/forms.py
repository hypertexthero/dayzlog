from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from dayzlog.apps.blog.models import Post, IS_DRAFT, IS_PUBLIC

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'slug', 'created_at', 'updated_at', 'publish', 
                    'content_html')

    def __init__(self, request, *args, **kwargs):
        self.user = request.user
        super(PostForm, self).__init__(request.POST or None, *args, **kwargs)
        self.fields['content_markdown'].widget.attrs['class'] = 'wmd-input'
        self.fields['content_markdown'].widget.attrs['id'] = 'wmd-input'