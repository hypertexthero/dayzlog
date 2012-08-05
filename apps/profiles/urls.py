from django.conf.urls.defaults import *

from idios.views import ProfileListView, ProfileDetailView, ProfileUpdateView


urlpatterns = patterns("idios.views",
    url(r"^(?P<username>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    url(r"^(?P<profile_slug>[\w\._-]+)/up/(?P<profile_pk>\d+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    
    # url(r"^edit/(?P<username>[\w\._-]+)$", ProfileUpdateView.as_view(), name="profile_edit"),
    
    # url(r"^all/$", ProfileListView.as_view(all_profiles=True), 
    #         name="profile_list_all"),
    url(r"", include("idios.urls_base")),
    url(r"^(?P<profile_slug>[\w\._-]+)/", include("idios.urls_base")),
)
