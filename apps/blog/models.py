from datetime import datetime
from django.template.defaultfilters import slugify
from BeautifulSoup import BeautifulSoup

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from voting.models import Vote
from voting.managers import VoteManager

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

STATUS_CHOICES = (
    (IS_DRAFT, _("Draft")), 
    (IS_PUBLIC, _("Public")),
    # (IS_DELETED, _("Deleted")) # =todo: remove this
)

class HotManager(VoteManager):
    def get_top(self):
        return self

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

    votes = models.ForeignKey(Vote, related_name='votes', null=True, blank=True)

    objects = models.Manager()
    hot = HotManager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        # =todo: order by highest score
        # order_with_respect_to = 'votes'
        # ordering = ('hot',)
        # get_latest_by = 'updated_at'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_user_post_detail', None, {
            'username': self.author.username,
            'slug': self.slug,
        })

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