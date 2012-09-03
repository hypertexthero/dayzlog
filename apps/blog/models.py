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

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import markdown
from typogrify.templatetags.typogrify_tags import typogrify

# defining html sanitizer to subsequently use in content_markdown to content_html conversion of user content at post save
# http://code.google.com/p/html5lib/wiki/UserDocumentation
# http://djangosnippets.org/snippets/2444/
import html5lib
from html5lib import sanitizer
def sanitize(value):
    p = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    return p.parseFragment(value).toxml()

IS_DRAFT = 1
IS_PUBLIC = 2

STATUS_CHOICES = (
    (IS_DRAFT, _("Draft")), 
    (IS_PUBLIC, _("Published")),
)

class VoteAwareManager(models.Manager):
    """ Get top votes. hot = VoteAwareManager() """
    def _get_score_annotation(self): # http://stackoverflow.com/questions/1301346/the-meaning-of-a-single-and-a-double-underscore-before-an-object-name-in-python
        model_type = ContentType.objects.get_for_model(self.model)
        table_name = self.model._meta.db_table
        return self.extra(select={
            'score': 'SELECT COALESCE(SUM(vote),0) FROM %s WHERE content_type_id=%d AND object_id=%s.id' %
                (Vote._meta.db_table, int(model_type.id), table_name)}
        )

    def most_hated(self):
        return self._get_score_annotation().order_by('score')

    def most_loved(self):
        return self._get_score_annotation().order_by('-score')

class Post(models.Model):
    """Post model"""
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), blank=True)
    author = models.ForeignKey(User, related_name="added_posts")
    creator_ip = models.CharField(_("IP Address of the Post Creator"), max_length=255, blank=True, null=True)
    content_markdown = models.TextField(_("Entry"), blank=True, help_text="<a data-toggle='modal' href='#markdownhelp'>markdown syntax</a>")
    content_html = models.TextField(blank=True, null=True, editable=False)
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=IS_DRAFT)
    publish = models.DateTimeField(_("publish"), default=datetime.now)
    created_at = models.DateTimeField(_("created at"), default=datetime.now)
    updated_at = models.DateTimeField(_("updated at"))

    # votes = generic.GenericRelation(Vote)

    objects = models.Manager()
    hot = VoteAwareManager()

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

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

    def is_public(self):
        return self.status == IS_PUBLIC
    
    def get_owners(self):
        return [self.author]

    # =todo: next/prev links
    # def get_next(self):
    #     next = Post.objects.filter(id__gt=self.id)
    #     if next:
    #         return next[0]
    #     return False
      
    # def get_prev(self):
    #     prev = Post.objects.filters(id__lt=self.id)
    #     if prev:
    #         return prev[0]
    #     return False