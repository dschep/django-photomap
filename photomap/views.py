import json
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from PIL import Image

from .models import Photo

class MapView(TemplateView):
    template_name = 'photomap/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(settings.PHOTOMAP_OPTIONS)
        return context

def thumb(request, image_id):
    image = get_object_or_404(Photo, pk=image_id).image
    #image.resize()
    strio = StringIO()
    image.save(strio)
    strio.seek(0)
    return HttpResponse(strio)#, content_type=??)
