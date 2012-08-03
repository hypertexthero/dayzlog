from django.db import models
from django.db.models import permalink
from markdown import markdown
import datetime
from typogrify.templatetags.typogrify_tags import typogrify

class Note(models.Model):
    
    KIND = (
        ('L', 'Link'),
        ('A', 'Article'),
    )
    
    """Model to save our note"""
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=1, choices=KIND, default=1, help_text="Is this a link to other content or an original article?")
    # TODO: linkurl field and link/article slug
    url = models.URLField(blank=True, help_text="The link URL")
    # slug = models.SlugField(unique_for_date='pub_date', help_text='Must be unique for the publication date.')
    content_markdown = models.TextField(blank=True, verbose_name='Note (markdown syntax)')
    content_html = models.TextField(editable=False) 
    # created = models.DateTimeField(default=datetime.datetime.now)
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now_add=True, editable=False)
    #automatically add timestamps when object is created
    # created = models.DateTimeField(auto_now_add=True) 
    #automatically add timestamps when object is updated
    # modified = models.DateTimeField(auto_now=True)

    # display correct plural name in admin
    class Meta:
        ordering = ['modified']
        verbose_name_plural = "notes"

    # TODO: Combine django static generator in ~/django_projects/victoreskinazi.com with the functionality below so we are serving static files in HTML on server and Markdown and HTML columns in database. Also try to find a way to have static files in Markdown format on the server.
    # https://code.djangoproject.com/wiki/UsingMarkup
    def save(self):
        # Also applying codehilite and footnotes markdown extensions: 
            # http://fi.am/entry/code-highlighting-in-django/
            # http://freewisdom.org/projects/python-markdown/CodeHilite
            # http://freewisdom.org/projects/python-markdown/Footnotes
            # typogrify - http://code.google.com/p/typogrify/ and http://djangosnippets.org/snippets/381/
        self.content_html = typogrify(markdown(self.content_markdown, ['footnotes', 'tables', 'nl2br', 'codehilite']))
        # self.content_html = markdown(self.content_markdown)
        self.modified = datetime.datetime.now()
        super(Note, self).save()

    # display note title in admin
    def __unicode__(self):
        return self.title


# http://djangosnippets.org/snippets/2047/
# TODO: http://www.michelepasin.org/techblog/2009/08/06/representing-hierarchical-data-with-django-and-mptt/
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

class MenuItemManager(models.Manager):
    def get_query_set(self):
        return super(MenuItemManager, self).get_query_set().order_by("order", "id")

class MenuItem(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="Name")
    order = models.IntegerField(blank = True, null = True)
    
    objects = MenuItemManager()
    order_field = 'order' # You can specify your own field for sorting, but it's 'order' by default

    class Meta:
        db_table = u"menu"
    
    def __unicode__(self):
        return u"%s" % self.name
        
    def order_link(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        obj_id = self.id
        kwargs = {"model_type_id": model_type_id}
        url = reverse("admin_order", kwargs=kwargs)
        return '<a href="%s" class="order_link">%s</a>' % (url, str(self.pk) or '')
    order_link.allow_tags = True
    order_link.short_description = 'Order' # If you change this you should change admin_sorting.js too

