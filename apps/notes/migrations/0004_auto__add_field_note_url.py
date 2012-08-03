# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Note.url'
        db.add_column('notes_note', 'url', self.gf('django.db.models.fields.URLField')(default='http://link.tld', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Note.url'
        db.delete_column('notes_note', 'url')


    models = {
        'notes.note': {
            'Meta': {'ordering': "['modified']", 'object_name': 'Note'},
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'content_markdown': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "'http://link.tld'", 'max_length': '200'})
        }
    }

    complete_apps = ['notes']
