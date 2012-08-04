from models import Note
from django.contrib import admin

class NoteAdmin(admin.ModelAdmin):
    # fields = ('title', 'url', 'created')
    list_display = ('title', 'status', 'created', 'modified')
    # date_hierarchy = 'modified'
    # list_filter = ('title', 'kind', 'url', 'created', 'modified')

admin.site.register(Note, NoteAdmin)