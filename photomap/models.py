from django.contrib.gis.db import models
from stdimage import StdImageField

class Photo(models.Model):
    image = StdImageField(upload_to='map-photo', variations={
        'thumbnail': (50, 50, True),
        })
    location = models.PointField(srid=4326, null=True)
    user_session_key = models.CharField(max_length=40, null=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return "Image('{0.image.name}', '{0.location}')".format(self)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django\.contrib\.gis"])
