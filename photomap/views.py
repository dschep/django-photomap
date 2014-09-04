import json

from six import BytesIO

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from PIL import Image, ImageOps

from .models import Photo, PhotoMapConf

class MapView(TemplateView):
    template_name = 'photomap/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(PhotoMapConf().configured_data)
        return context
