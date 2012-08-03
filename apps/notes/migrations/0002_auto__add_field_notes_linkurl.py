# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Notes.linkurl'
        db.add_column('notes_notes', 'linkurl', self.gf('django.db.models.fields.URLField')(default='http://link.tld', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Notes.linkurl'
        db.delete_column('notes_notes', 'linkurl')


    models = {
        'notes.notes': {
            'Meta': {'ordering': "['modified']", 'object_name': 'Notes'},
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'content_markdown': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '1'}),
            'linkurl': ('django.db.models.fields.URLField', [], {'default': "'http://link.tld'", 'max_length': '200'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['notes']
