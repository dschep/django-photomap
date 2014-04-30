# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.gis.geos import geometry
from PIL import Image
from PIL.ExifTags import TAGS
from ..util import point_from_exif

class Migration(DataMigration):

    def forwards(self, orm):
        for photo in orm['photomap.Photo'].objects.all():
            photo.location = point_from_exif(photo.image.path)
            photo.save()

    def backwards(self, orm):
        raise NotImplementedError('Too lazy to write a method to write the'
                                  ' coordinates to the EXIF of the files')

    models = {
        u'photomap.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'})
        }
    }

    complete_apps = ['photomap']
    symmetrical = True
