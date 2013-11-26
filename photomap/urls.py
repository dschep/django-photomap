from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .views import MapView
from .api import PhotoResource

v1_api = Api(api_name='v1')
v1_api.register(PhotoResource())

urlpatterns = patterns('photomap.views',
    url(r'^$', MapView.as_view(), name='map'),
    url(r'^api/', include(v1_api.urls)),
)
