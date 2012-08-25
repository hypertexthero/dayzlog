from django.contrib import admin

from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'content_markdown')

admin.site.register(Post, PostAdmin)
