from django.urls import path
from django.conf.urls import url
from .views import liveSettingView, updateEmotionData

app_name = 'liveSetting'

urlpatterns = [
    url(r'^(?P<streamerName>[^/]+)/$', liveSettingView.as_view(), name='liveSettingView'),
    url(r'^(?P<streamerName>[^/]+)/updateEmotionData$', updateEmotionData),
]
