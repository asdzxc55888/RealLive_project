from django.urls import path, include
from django.conf.urls import url
from .views import passwordResetView

app_name = 'passwordReset'

urlpatterns = [
    path('', passwordResetView),
]
