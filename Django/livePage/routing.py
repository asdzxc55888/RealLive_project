from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/live/(?P<streamerName>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/liveSetting/(?P<streamerName>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/live/(?P<streamerName>[^/]+)/image$', consumers.ImageConsumer),
]
