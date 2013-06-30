# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field _children on 'Commit'
        m2m_table_name = db.shorten_name(u'repokarma_commit__children')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_commit', models.ForeignKey(orm['repokarma.commit'], null=False)),
            ('to_commit', models.ForeignKey(orm['repokarma.commit'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_commit_id', 'to_commit_id'])


    def backwards(self, orm):
        # Removing M2M table for field _children on 'Commit'
        db.delete_table(db.shorten_name(u'repokarma_commit__children'))


    models = {
        'repokarma.commit': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Commit'},
            '_children': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['repokarma.Commit']", 'symmetrical': 'False'}),
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