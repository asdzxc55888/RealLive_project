from django.urls import path
from django.conf.urls import url
from .views import liveView

app_name = 'live'

urlpatterns = [
    #path('<str:streamerName>', liveView.as_view()),
    url(r'^(?P<streamerName>[^/]+)/$', liveView.as_view(), name='liveView'),
]
