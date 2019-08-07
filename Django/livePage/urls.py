from django.urls import path
from django.conf.urls import url
from .views import liveView

app_name = 'live'

urlpatterns = [
    url(r'^(?P<streamerName>[^/]+)/$', liveView.as_view(), name='liveView'),
]
