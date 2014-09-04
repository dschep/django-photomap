from django.contrib.gis.db import models
from stdimage import StdImageField
from appconf import AppConf

class PhotoMapConf(AppConf):
    MAP_CENTER = [38.91, -77.04]
    DEFAULT_ZOOM = 13,
    MAP_TITLE = 'Photo Map'
    ABOUT = """
        <p>
            Built by <a href="http://github.com/dschep">Daniel Schep</a> using
            Leaflet, Bootstrap, Django & GeoDjango. Souce available on
            <a href="http://github.com/dschep/dc-bikelane-graffiti-map"
                target="_blank">Github</a>.
        </p>
    """
    LOGO = ''

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
