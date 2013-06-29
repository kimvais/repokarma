# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Commit.files'
        db.delete_column(u'repokarma_commit', 'files')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Commit.files'
        raise RuntimeError("Cannot reverse this migration. 'Commit.files' and its values cannot be restored.")

    models = {
        'repokarma.commit': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Commit'},
            'description': ('django.db.models.fields.TextField', [], {}),
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