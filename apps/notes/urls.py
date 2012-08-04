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
 
    url(r'^$', views.notes_list, name='notes_list'),  
    url(r'^archive/$', views.notes_archive, name='notes_archive'),  
    # url(r'^$', 'django.views.generic.date_based.archive_index', entry_info_dict, name='notes_list'),
    url(r'^archive/(?P<id>\d+)/$', views.notes_detail, name='notes_detail'),  
    url(r'^new/$', views.notes_create, name='notes_create'),  
    url(r'^edit/(?P<id>\d+)/$', views.notes_edit, name='notes_edit'),  
    url(r'^delete/(?P<id>\d+)/$', views.notes_delete, name='notes_delete'), 
    url(r'^search/$', views.search, name="notes_search"),
)