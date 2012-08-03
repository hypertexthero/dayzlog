from blog.models import Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    # fields = ('title', 'url', 'created')
    list_display = ('title', 'created', 'modified')
    # date_hierarchy = 'modified'
    # list_filter = ('title', 'kind', 'url', 'created', 'modified')

admin.site.register(Post, PostAdmin)