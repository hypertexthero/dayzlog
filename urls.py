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

urlpatterns = patterns("",
    # url(r"^$", direct_to_template, {
    #     "template": "homepage.html",
    # }, name="home"),
    url(r"^$", "blog.views.homepage", name="home"), 
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("profiles.urls")), # NOTA BENE: that this is pointing to profiles/urls.py and not IDIOS app...
    # url(r"^up/", include("profiles.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    # url(r'^notes/', include('notes.urls')),
    # url(r'^log/', include('blog.urls')),
    url(r'^logs/', include('blog.urls')), 
    # url(r'^b/', include('blogs.short_urls')), # For short urls, if you want 
    url(r'^feeds/posts/(?P<url>w+)/', 'django.contrib.syndication.views.feed', blogs_feed_dict),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
