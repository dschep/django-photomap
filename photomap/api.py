from tastypie.contrib.gis.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Photo
from .util import (MultipartResource, UserSessionKeyAuthorization,
                   geojson_from_exif, NoGPSInfoException)
from django.contrib.gis.geos import geometry

class PhotoAuthorization(UserSessionKeyAuthorization):
    """ We don't want to allow users to delete photos """

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")


class PhotoResource(MultipartResource, ModelResource):
    class Meta:
        queryset = Photo.objects.all()
        authorization = PhotoAuthorization(
                session_key_field='user_session_key')

    def dehydrate(self, bundle):
        """ Don't return session keys """
        del bundle.data['user_session_key']
        return bundle

    def obj_create(self, bundle, **kwargs):
        # set the session key from cookies
        return super(PhotoResource, self).obj_create(
                bundle, user_session_key=bundle.request.session.session_key)

    def hydrate_image(self, bundle):
        if 'image' in bundle.data:
            try:
                bundle.data['location'] = geojson_from_exif(
                        bundle.data['image'])
            except NoGPSInfoException:
                pass
        return bundle
