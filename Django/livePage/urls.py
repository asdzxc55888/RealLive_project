from django.urls import path
from .views import liveView

app_name = 'live'

urlpatterns = [
    path('<str:streamerName>', liveView.as_view()),
]
