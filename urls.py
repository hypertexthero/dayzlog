from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.generic.date_based import archive_index
from dayzlog.apps.blog import views
from django.contrib import admin
admin.autodiscover()
from pinax.apps.account.openid_consumer import PinaxConsumer

handler500 = "pinax.views.server_error"

from dayzlog.apps.blog.feeds import BlogFeedUser
blogs_feed_dict = {"feed_dict": {
    'only': BlogFeedUser,
    }}

from dayzlog.apps.blog.models import Post, IS_PUBLIC
post_dict_public = {
    'queryset': Post.objects.filter(status=IS_PUBLIC),
    'template_object_name': 'post',
}
post_dict = {
    'queryset': Post.objects.filter(),
    'template_object_name': 'post',
}

# =todo: vanity url: http://stackoverflow.com/questions/3333765/get-user-from-url-segment-with-django 

urlpatterns = patterns("",

    url(r"^$", "dayzlog.apps.blog.views.homepage", name="home"),
    url(r"^new/$", "dayzlog.apps.blog.views.new", name="new"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    # url(r"^about/", include("about.urls")),
    url(r"^faq/$", direct_to_template, {"template": "faq.html"}, name="faq"),
    # url(r"^beans/$", direct_to_template, {"template": "beans.html"}, name="beans"),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("profiles.urls")), # NOTA BENE: that this is pointing to profiles/urls.py and not IDIOS app...
    # url(r"^up/", include("profiles.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    # url(r'^log/', include('blog.urls')),
    url(r'^logs/', include('dayzlog.apps.blog.urls')),
    url(r'^relationships/', include('relationships.urls')),
    url(r'^following/','dayzlog.apps.blog.views.following', name='following'),
    url(r'^followers/','dayzlog.apps.blog.views.followers', name='followers'),
    url(r'^backup/$', 'dayzlog.apps.blog.views.backup', name='backup'),
    url(r'^dashboard/$', 'dayzlog.apps.blog.views.dashboard', dict(post_dict, template_name='blog/dashboard.html'), name='dashboard'),
    url(r'^write/$', 'dayzlog.apps.blog.views.add', name='blog_add'),
    # url(r'^b/', include('blogs.short_urls')), # For short urls, if you want
    url(r'^feeds/posts/(?P<url>w+)/', 'django.contrib.syndication.views.feed', blogs_feed_dict),
    url(r'^search/$', 'dayzlog.apps.blog.views.search', name="search"),
    
    # webmaster tools site verification
    # http://news.e-scribe.com/431
    url(r'^googleab865041b72036e4\.html$', lambda r: HttpResponse("google-site-verification: googleab865041b72036e4.html", mimetype="text/html"))
    )

# if settings.SERVE_MEDIA:
#     urlpatterns += patterns("",
#         url(r"", include("staticfiles.urls")),
#     )

# =todo: figure out why I had to add this so player image is served
if settings.DEBUG :
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
