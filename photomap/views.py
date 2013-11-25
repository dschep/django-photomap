import json

from django.conf import settings

from django.views.generic import TemplateView

class MapView(TemplateView):
    template_name = 'photomap/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(settings.PHOTOMAP_OPTIONS)
        return context
