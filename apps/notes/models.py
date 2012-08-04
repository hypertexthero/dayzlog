from django.db import models
from django.db.models import permalink
from markdown import markdown
import datetime
from typogrify.templatetags.typogrify_tags import typogrify

class LiveNoteManager(models.Manager):
    """ Live and For Review note status """
    def get_query_set(self):
        return super(LiveNoteManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Note(models.Model):
    
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
    )    
    
    """Model to save our note"""
    title = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    # TODO: slug
    # slug = models.SlugField(unique_for_date='pub_date', help_text='Must be unique for the publication date.')
    content_markdown = models.TextField(blank=True, verbose_name='Note (markdown syntax)')
    content_html = models.TextField(editable=False) 
    created = models.DateTimeField(default=datetime.datetime.now)
    modified = models.DateTimeField(auto_now_add=True, editable=False)

    # Need to be this way around so that non-live notes will show up in Admin, which uses the default (first) manager.
    objects = models.Manager()
    live = LiveNoteManager()

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


#     # def live_note_set(self):
#     #     from notes.models import Note
#     #     return self.note_set.filter(status=Note.LIVE_STATUS)
    