# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.location'
        db.add_column(u'photomap_photo', 'location',
                      self.gf('django.contrib.gis.db.models.fields.PointField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Photo.location'
        db.delete_column(u'photomap_photo', 'location')


    models = {
        u'photomap.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'})
        }
    }

    complete_apps = ['photomap']