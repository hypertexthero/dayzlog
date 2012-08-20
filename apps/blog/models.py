from datetime import datetime
from django.template.defaultfilters import slugify
from BeautifulSoup import BeautifulSoup

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

import markdown
# from django.contrib.markup.templatetags.markup import markdown
from typogrify.templatetags.typogrify_tags import typogrify

# defining html sanitizer to subsequently use in content_markdown to content_html conversion of user content at post save
# http://code.google.com/p/html5lib/wiki/UserDocumentation
# http://djangosnippets.org/snippets/2444/
import html5lib
from html5lib import sanitizer
def sanitize(value):
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    return p.parseFragment(value).toxml()


# IS_DELETED = 0
IS_DRAFT = 1
IS_PUBLIC = 2

class Blog(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'))
    icon = models.ImageField(_('blog icon'), height_field=None, width_field=None, blank=True, upload_to="blog_icons/", default="blog_icons/default.jpg")
    description = models.TextField(_('description'), max_length=256, blank=True)
    
    # TODO: Made moderators
    # TODO: Made list of who can write to blog (empty - every one)
    # TODO: Or just made gerenal access rights - who can view,write,comment on this blog
    #moderators = models.ManyToMany()

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
    
    @models.permalink
    def get_absolute_url(self):
        return ('blog_blog_detail', None, {
            'slug': self.slug
            })

    def __unicode__(self):
        return self.name

    def get_last_post(self):
        post = self.post_list.filter(status=IS_PUBLIC)[:1]
        if post:
            return post[0]
        return None


STATUS_CHOICES = (
    (IS_DRAFT, _("Draft")), 
    (IS_PUBLIC, _("Public")),
    # (IS_DELETED, _("Deleted")) # =todo: remove this
)

class Post(models.Model):
    """Post model."""
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), blank=True)
    author = models.ForeignKey(User, related_name="added_posts")
    creator_ip = models.CharField(_("IP Address of the Post Creator"), max_length=255, blank=True, null=True)
    tease = models.TextField(_('tease'), blank=True)
    # body = models.TextField(_('body'))
    content_markdown = models.TextField(blank=True, verbose_name='Entry', help_text="<a data-toggle='modal' href='#markdownhelp'>markdown syntax</a>")
    content_html = models.TextField(blank=True, null=True, editable=False)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=IS_DRAFT)
    publish = models.DateTimeField(_('publish'), default=datetime.now)
    created_at = models.DateTimeField(_('created at'), default=datetime.now)
    updated_at = models.DateTimeField(_('updated at'))
    blog = models.ForeignKey(Blog, related_name='post_list', null=True, blank=True)
    last_comment_datetime = models.DateTimeField(_('date of last comment'), default=datetime.now)
    
    # rating = RatingField()
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-updated_at',)
        get_latest_by = 'updated_at'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if self.blog:
            return ('blog_post_detail', None, {
                'blog': self.blog.slug,
                'slug': self.slug,
            })
        else:
            return ('blog_user_post_detail', None, {
                'username': self.author.username,
                'slug': self.slug,
            })

# # =todo: add markdown and html dual db fields, show markdown when user is editing, html when page is displayed
# # # TODO: Combine django static generator in ~/django_projects/victoreskinazi.com with the functionality below so we are serving static files in HTML on server and Markdown and HTML columns in database. Also try to find a way to have static files in Markdown format on the server.
#     # https://code.djangoproject.com/wiki/UsingMarkup
#     def save(self):
#         # Also applying codehilite and footnotes markdown extensions: 
#             # http://fi.am/entry/code-highlighting-in-django/
#             # http://freewisdom.org/projects/python-markdown/CodeHilite
#             # http://freewisdom.org/projects/python-markdown/Footnotes
#             # typogrify - http://code.google.com/p/typogrify/ and http://djangosnippets.org/snippets/381/
#         self.content_html = typogrify(markdown(self.content_markdown, ['footnotes', 'tables', 'nl2br', 'codehilite']))
#         # self.content_html = markdown(self.content_markdown)
#         self.modified = datetime.datetime.now()
#         super(Note, self).save()

    def save(self, force_insert=False, force_update=False, update_date=True):
        # http://www.freewisdom.org/projects/python-markdown/Extra
        self.content_html = sanitize(typogrify(markdown.markdown(self.content_markdown, ["safe", "extra", "footnotes", "tables", "nl2br", "codehilite"])))
        
        if update_date:
            self.updated_at = datetime.now()
        if (self.slug == None or self.slug == ''):
            if not self.id:
                super(Post, self).save(force_insert, force_update)
            self.slug = '%d-%s' % (self.id, slugify(self.title))

        super(Post, self).save(force_insert, force_update)


        # if self.tease:
        #     editor_cut = self.body.find('<hr class="editor_cut"/>')
        #     if editor_cut != -1:
        #         self.tease = self.body[:editor_cut]
        # self.body = clear_html_code(self.body)
        # self.tease = clear_html_code(self.tease)
        # http://stackoverflow.com/questions/7035916/markdown-in-django-xss-safe


    def is_public(self):
        return self.status == IS_PUBLIC
    
    def get_owners(self):
        return [self.author]

    def get_next(self):
        next = Post.objects.filter(id__gt=self.id)
        if next:
            return next[0]
        return False
      
    def get_prev(self):
        prev = Post.objects.filters(id__lt=self.id)
        if prev:
            return prev[0]
        return False


