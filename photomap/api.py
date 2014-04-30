from tastypie.contrib.gis.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Photo
from .util import MultipartResource, UserSessionKeyAuthorization, geojson_from_exif
from django.contrib.gis.geos import geometry


class PhotoResource(MultipartResource, ModelResource):
    class Meta:
        queryset = Photo.objects.all()
        authorization = UserSessionKeyAuthorization()

    def dehydrate(self, bundle):
        """ Don't return session keys """
        del bundle.data['user_session_key']
        return bundle

    def obj_create(self, bundle, **kwargs):
        return super(PhotoResource, self).obj_create(bundle, user_session_key=bundle.request.session.session_key)

    def hydrate_image(self, bundle):
        if 'image' in bundle.data:
            bundle.data['location'] = geojson_from_exif(bundle.data['image'])
        return bundle
