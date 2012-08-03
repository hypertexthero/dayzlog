from django.conf.urls.defaults import *
 
import views

# from notes.models import Note 
# entry_info_dict = { 
#     'queryset': Note.objects.all(), 
#     'date_field': 'modified', 
#     'template_name': 'notes/list.html',
#     'allow_future': False,
#     }

# TODO: implement article and link archives

urlpatterns = patterns('', 
 
    url(r'^$', views.posts_list, name='posts_list'),  
    url(r'^archive/$', views.posts_archive, name='posts_archive'),  
    # url(r'^$', 'django.views.generic.date_based.archive_index', entry_info_dict, name='posts_list'),
    url(r'^archive/(?P<id>\d+)/$', views.posts_detail, name='posts_detail'),  
    url(r'^new/$', views.posts_create, name='posts_create'),  
    url(r'^update/(?P<id>\d+)/$', views.posts_update, name='posts_update'),  
    url(r'^delete/(?P<id>\d+)/$', views.posts_delete, name='posts_delete'), 
    url(r'^search/$', views.search, name="posts_search"),
)