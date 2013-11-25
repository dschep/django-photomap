from django.conf.urls import patterns, include, url

from .views import MapView

urlpatterns = patterns('photomap.views',
    url(r'^$', MapView.as_view(), name='map'),
)
