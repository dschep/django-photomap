from django.contrib.gis.db import models

class Photo(models.Model):
    image = models.ImageField(upload_to='map-photo')
    location = models.PointField(srid=4326, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return "Image('{0.image.name}', '{0.location}')".format(self)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django\.contrib\.gis"])
