from django.urls import path, include
from django.conf.urls import url
from .views import passwordResetView
from django.contrib.auth.views import password_reset

app_name = 'passwordReset'

urlpatterns = [
    path('', password_reset),
]
