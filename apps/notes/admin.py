from models import Note, MenuItem
from django.contrib import admin

class NoteAdmin(admin.ModelAdmin):
    # fields = ('title', 'url', 'created')
    list_display = ('title', 'kind', 'url', 'created', 'modified')
    # date_hierarchy = 'modified'
    # list_filter = ('title', 'kind', 'url', 'created', 'modified')

admin.site.register(Note, NoteAdmin)

# http://djangosnippets.org/snippets/2047/
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order_link')
    list_display_links = ('id', 'name')
    ordering = ('order','id')
    
    class Media:
      js = ("/static/js/jquery-1.7.1.min.js",
            "/static/js/jquery-ui-1.8.20.custom.min.js",
            "/static/js/admin_sorting.js",)

admin.site.register(MenuItem, MenuItemAdmin)

