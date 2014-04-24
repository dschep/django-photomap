from django.db import models

from PIL import Image
from PIL.ExifTags import TAGS

class Photo(models.Model):
    image = models.ImageField(upload_to='map-photo')

    @property
    def location(self):
        tags = {TAGS.get(t): v for t, v in
                Image.open(self.image.path)._getexif().items()}

        n_sec = tags['GPSInfo'][2][2][0] / float(tags['GPSInfo'][2][2][1])
        n_min = tags['GPSInfo'][2][1][0] / float(tags['GPSInfo'][2][1][1])
        n_deg = tags['GPSInfo'][2][0][0] / float(tags['GPSInfo'][2][0][1])
        w_sec = tags['GPSInfo'][4][2][0] / float(tags['GPSInfo'][4][2][1])
        w_min = tags['GPSInfo'][4][1][0] / float(tags['GPSInfo'][4][1][1])
        w_deg = tags['GPSInfo'][4][0][0] / float(tags['GPSInfo'][4][0][1])

        lat = n_deg + (n_min + n_sec/60.0)/60.0
        lng = w_deg + (w_min + w_sec/60.0)/60.0

        if tags['GPSInfo'][1] != 'N':
            lat *= -1
        if tags['GPSInfo'][3] != 'E':
            lng *= -1

        return [lat, lng]
