from django.urls import path
from .views import livePage_view

app_name = 'live'

urlpatterns = [
    path('<str:streamerName>', livePage_view),
]
