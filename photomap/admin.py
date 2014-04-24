from django.contrib import admin

from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'preview', 'location')
    readonly_fields = ('preview', 'location')
    def preview(self, obj):
        return '<img height="250" src="{0}">'.format(obj.image.url)
    preview.allow_tags = True

admin.site.register(Photo, PhotoAdmin)
