from tastypie.resources import ModelResource
from tastypie import fields
from .models import Photo
from .util import MultipartResource
from django.contrib.gis.geos import geometry


class PhotoResource(MultipartResource, ModelResource):
    class Meta:
        queryset = Photo.objects.all()

    def dehydrate_location(self, bundle):
        """ flip coordinate order since leaflet expects lat,lng not lng,lat """
        if bundle.obj.location is not None:
            return [bundle.obj.location.y, bundle.obj.location.x]

    def hydrate_location(self, bundle):
        """ create a Point object from an array """
        if 'location' in bundle.data:
            bundle.data['location'] = geometry.Point(
                x=bundle.data['location'][1],
                y=bundle.data['location'][0],
                srid=4326,
                )

        return bundle
