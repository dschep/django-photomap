from tastypie.resources import ModelResource
from tastypie import fields
from .models import Photo


class PhotoResource(ModelResource):
    class Meta:
        queryset = Photo.objects.all()

    def dehydrate_location(self, bundle):
        """ flip coordinate order since leaflet expects lat,lng not lng,lat """
        return [bundle.obj.location.y, bundle.obj.location.x]
