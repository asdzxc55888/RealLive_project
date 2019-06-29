# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/liveChat/', consumers.ChatConsumer),
]