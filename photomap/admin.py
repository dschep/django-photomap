from django.contrib.gis import admin

from .models import Photo


class PhotoAdmin(admin.OSMGeoAdmin):
    list_display = ('image', 'preview', 'location')
    def preview(self, obj):
        try:
            return '<img src="{0}">'.format(obj.image.admin.url)
        except ValueError:
            return ''
    preview.allow_tags = True

admin.site.register(Photo, PhotoAdmin)
