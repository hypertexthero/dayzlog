from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.date_based import archive_index
from blog import views
from django.contrib import admin
admin.autodiscover()
from pinax.apps.account.openid_consumer import PinaxConsumer

handler500 = "pinax.views.server_error"

from blog.feeds import BlogFeedAll, BlogFeedBlog, BlogFeedUser
blogs_feed_dict = {"feed_dict": {
'all': BlogFeedAll, 'blog' : BlogFeedBlog, 'only': BlogFeedUser,
}}

# =todo: vanity url: http://stackoverflow.com/questions/3333765/get-user-from-url-segment-with-django 

# =voting
# http://code.google.com/p/django-voting/wiki/RedditStyleVoting
# from django.views.generic.list_detail import object_list
# from blog.models import Post
# from voting.views import vote_on_object

urlpatterns = patterns("",
    # url(r"^$", direct_to_template, {
    #     "template": "homepage.html",
    # }, name="home"),
    url(r"^$", "blog.views.homepage", name="home"), 
    # url(r"^popular/$", "blog.views.popular", name="popular"), 
    
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("profiles.urls")), # NOTA BENE: that this is pointing to profiles/urls.py and not IDIOS app...
    # url(r"^up/", include("profiles.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    # url(r'^log/', include('blog.urls')),
    
    # Generic view to list Link objects
    # url(r'^logs/$', object_list, dict(queryset=Post.objects.all(),
    #     template_object_name='post', template_name='blog/all.html',
    #     paginate_by=15, allow_empty=True)),
    
    # =voting
    # url(r"^logs/(?P<username>[\w\._\-]+)/(?P<slug>[-\w]+)/(?P<direction>up|down|clear)vote/?$", vote_on_object, 
    #     dict(model=Post, 
    #         template_object_name="post",
    #         template_name="blog/blog_confirm_vote.html",
    #         allow_xmlhttprequest=True)),
    
    url(r'^logs/', include('blog.urls')), 
    # url(r'^b/', include('blogs.short_urls')), # For short urls, if you want 
    url(r'^feeds/posts/(?P<url>w+)/', 'django.contrib.syndication.views.feed', blogs_feed_dict),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
