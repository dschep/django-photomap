from tastypie.resources import ModelResource
from tastypie import fields
from .models import Photo


class PhotoResource(ModelResource):
    location = fields.CharField(attribute='location', readonly=True)
    class Meta:
        queryset = Photo.objects.all()

    def dehydrate_location(self, bundle):
        """ Don't dehydrate the list, it's already valid """
        return bundle.obj.location
