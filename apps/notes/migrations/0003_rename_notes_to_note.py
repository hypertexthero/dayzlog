# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('notes_notes', 'notes_note')


    def backwards(self, orm):
        db.rename_table('notes_note','notes_notes')

    # def forwards(self, orm):
    #     
    #     # Deleting model 'Notes'
    #     db.delete_table('notes_notes')
    # 
    #     # Adding model 'Note'
    #     db.create_table('notes_note', (
    #         ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
    #         ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
    #         ('kind', self.gf('django.db.models.fields.CharField')(default=1, max_length=1)),
    #         ('content_markdown', self.gf('django.db.models.fields.TextField')()),
    #         ('content_html', self.gf('django.db.models.fields.TextField')()),
    #         ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
    #         ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
    #     ))
    #     db.send_create_signal('notes', ['Note'])
    # 
    # 
    # def backwards(self, orm):
    #     
    #     # Adding model 'Notes'
    #     db.create_table('notes_notes', (
    #         ('kind', self.gf('django.db.models.fields.CharField')(default=1, max_length=1)),
    #         ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
    #         ('content_markdown', self.gf('django.db.models.fields.TextField')()),
    #         ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
    #         ('linkurl', self.gf('django.db.models.fields.URLField')(default='http://link.tld', max_length=200)),
    #         ('content_html', self.gf('django.db.models.fields.TextField')()),
    #         ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
    #         ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
    #     ))
    #     db.send_create_signal('notes', ['Notes'])
    # 
    #     # Deleting model 'Note'
    #     db.delete_table('notes_note')


    models = {
        'notes.note': {
            'Meta': {'ordering': "['modified']", 'object_name': 'Note'},
            'content_html': ('django.db.models.fields.TextField', [], {}),
            'content_markdown': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': '1', 'max_length': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['notes']
