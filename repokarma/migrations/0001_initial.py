# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EMail'
        db.create_table(u'repokarma_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='email', to=orm['repokarma.User'])),
        ))
        db.send_create_signal('repokarma', ['EMail'])

        # Adding model 'User'
        db.create_table(u'repokarma_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
        ))
        db.send_create_signal('repokarma', ['User'])

        # Adding model 'Repository'
        db.create_table(u'repokarma_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('repository_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'repokarma', ['Repository'])

        # Adding unique constraint on 'Repository', fields ['path', 'repository_type']
        db.create_unique(u'repokarma_repository', ['path', 'repository_type'])

        # Adding model 'Commit'
        db.create_table(u'repokarma_commit', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repokarma.Repository'])),
            ('nodeid', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repokarma.User'])),
            ('files', self.gf('django.db.models.fields.IntegerField')()),
            ('lines_added', self.gf('django.db.models.fields.IntegerField')()),
            ('lines_removed', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('repokarma', ['Commit'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repository', fields ['path', 'repository_type']
        db.delete_unique(u'repokarma_repository', ['path', 'repository_type'])

        # Deleting model 'EMail'
        db.delete_table(u'repokarma_email')

        # Deleting model 'User'
        db.delete_table(u'repokarma_user')

        # Deleting model 'Repository'
        db.delete_table(u'repokarma_repository')

        # Deleting model 'Commit'
        db.delete_table(u'repokarma_commit')


    models = {
        'repokarma.commit': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Commit'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'files': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'lines_added': ('django.db.models.fields.IntegerField', [], {}),
            'lines_removed': ('django.db.models.fields.IntegerField', [], {}),
            'nodeid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repokarma.Repository']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repokarma.User']"})
        },
        'repokarma.email': {
            'Meta': {'object_name': 'EMail'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'email'", 'to': "orm['repokarma.User']"})
        },
        u'repokarma.repository': {
            'Meta': {'unique_together': "(('path', 'repository_type'),)", 'object_name': 'Repository'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'repository_type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'repokarma.user': {
            'Meta': {'object_name': 'User'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['repokarma']