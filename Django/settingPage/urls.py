from django.urls import path
from .views import settingView, modifyPasswordView, streamSettingView, BecomeStreamer

app_name = 'setting'

urlpatterns = [
    path('', settingView.as_view()),
    path('stream', streamSettingView.as_view()),
    path('modifyPassword', modifyPasswordView.as_view()),
    path('BecomeStreamer', BecomeStreamer),
]
