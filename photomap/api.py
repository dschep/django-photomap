from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Photo
from .util import MultipartResource, UserSessionKeyAuthorization, point_from_exif
from django.contrib.gis.geos import geometry


class PhotoResource(MultipartResource, ModelResource):
    class Meta:
        queryset = Photo.objects.all()
        authorization = UserSessionKeyAuthorization()

    def dehydrate_location(self, bundle):
        """ flip coordinate order since leaflet expects lat,lng not lng,lat """
        if bundle.obj.location is not None:
            return [bundle.obj.location.y, bundle.obj.location.x]

    def hydrate_location(self, bundle):
        """
        create a Point object from an array
        unless it's already a point because it came from the image's EXIF
        """
        if 'location' in bundle.data and \
                not isinstance(bundle.data['location'], geometry.Point):
            bundle.data['location'] = geometry.Point(
                x=bundle.data['location'][1],
                y=bundle.data['location'][0],
                srid=4326,
                )

        return bundle

    def dehydrate(self, bundle):
        """ Don't return session keys """
        del bundle.data['user_session_key']
        return bundle

    def obj_create(self, bundle, **kwargs):
        return super(PhotoResource, self).obj_create(bundle, user_session_key=bundle.request.session.session_key)

    def hydrate_image(self, bundle):
        if 'image' in bundle.data:
            bundle.data['location'] = point_from_exif(bundle.data['image'])
        return bundle
