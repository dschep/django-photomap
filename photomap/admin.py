from django.contrib.gis import admin

from .models import Photo


class PhotoAdmin(admin.OSMGeoAdmin):
    list_display = ('image', 'preview', 'location')
    readonly_fields = ('preview',)
    def preview(self, obj):
        try:
            return '<img height="250" src="{0}">'.format(obj.image.url)
        except ValueError:
            return ''
    preview.allow_tags = True

admin.site.register(Photo, PhotoAdmin)
