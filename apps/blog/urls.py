from django.conf.urls.defaults import *
from django.conf import settings

from dayzlog.apps.blog.models import Post, IS_PUBLIC
from dayzlog.apps.profiles.models import Profile

# =voting
# http://code.google.com/p/django-voting/wiki/RedditStyleVoting
from django.views.generic.list_detail import object_list
from voting.views import vote_on_object
post_dict_vote = {
    'model': Post,
    # 'queryset': Post.objects.filter(status=IS_PUBLIC),
    'template_object_name': 'post',
    'slug_field': 'slug',
    'template_name': 'blog/post_confirm_vote.html',
    'allow_xmlhttprequest': 'true',
}

post_dict = {
    'queryset': Post.objects.filter(),
    'template_object_name': 'post',
}

backup_dict = {
    'queryset': Post.objects.filter(),
    'template_object_name': 'post',
    'template_name': 'blog/backup.txt',
}

post_dict_public = {
    'queryset': Post.objects.filter(status=IS_PUBLIC),
    'template_object_name': 'post',
    # 'extra_context': {"user": user},
}

urlpatterns = patterns('',
    # disabling viewing of list of all logs
    # url(r'^$', 'django.views.generic.list_detail.object_list', post_dict_public, name='blog_post_list'),
    url(r'^(?P<username>[\w\._\-]+)/$', 'blog.views.user_post_list', dict(post_dict_public, template_name='blog/user_post_list.html'), name='blog_user_post_list'),
    url(r'^edit/(?P<id>\d+)/$', 'blog.views.edit', name='blog_edit'),
    url(r'^(?P<action>draft|public)/(?P<id>\d+)/$', 'blog.views.change_status', name='blog_change_status'),
    url(r'^delete/(?P<id>\d+)/$', 'blog.views.delete', name='blog_delete'), 
    # =voting
    url(r'^(?P<slug>[-\w]+)/(?P<direction>up|down|clear)vote/?$', vote_on_object, post_dict_vote, name='post_voting'),
    # needs to come after the above otherwise post detail url doesn't work
    
    url(r'^(?P<username>[\w\._\-]+)/(?P<slug>[-\w]+)/$', 'blog.views.blog_user_post_detail', post_dict, name='blog_user_post_detail'),
   )

