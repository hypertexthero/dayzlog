# from django.conf.urls.defaults import *
# 
# from idios.views import ProfileListView, ProfileDetailView, ProfileUpdateView
# 
# 
# urlpatterns = patterns("idios.views",
#     url(r"^(?P<username>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),
#     url(r"^(?P<profile_slug>[\w\._-]+)/up/(?P<profile_pk>\d+)/$", ProfileDetailView.as_view(), name="profile_detail"),
#     
#     # url(r"^edit/(?P<username>[\w\._-]+)$", ProfileUpdateView.as_view(), name="profile_edit"),
#     
#     # url(r"^all/$", ProfileListView.as_view(all_profiles=True), 
#     #         name="profile_list_all"),
#     url(r"", include("idios.urls_base")),
#     url(r"^(?P<profile_slug>[\w\._-]+)/", include("idios.urls_base")),
# )

from django.conf.urls.defaults import *
from idios.views import ProfileListView, ProfileDetailView, ProfileUpdateView

# for squad.xml and squad.dtd generation - took view code from idios.views
from django.views.generic.detail import DetailView
from dayzlog.apps.profiles.views import SquadXMLView
from dayzlog.apps.profiles.models import Profile
from django.views.generic.simple import direct_to_template

urlpatterns = patterns("idios.views",
    
    # disabling ability to view list of all user profiles
    # url(r"^$", ProfileListView.as_view(all_profiles=True), name="profile_list_all"),
    
    # url(r"^(?P<profile_slug>[\w\._-]+)/", include("idios.urls_base")),
    # url(r"^(?P<profile_slug>[\w\._-]+)/(?P<profile_pk>\d+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    # url(r"", include("idios.urls_base")),
    
    url(r"^(?P<username>[\w\._-]+)/$", ProfileDetailView.as_view(), name="profile_detail"),
    url(r"^edit/(?P<username>[\w\._-]+)$", ProfileUpdateView.as_view(), name="profile_edit"),
)

# for squad.xml and squad.dtd generation - took view code from idios.views
urlpatterns += patterns("profiles.views",
    url(r"^(?P<username>[\w\._-]+)/squad.dtd$", direct_to_template, {"template": "profiles/squad.dtd",}, name="squaddtd"),
    url(r"^(?P<username>[\w\._-]+)/squad.xml$", SquadXMLView.as_view(), name="squadxml"),
)