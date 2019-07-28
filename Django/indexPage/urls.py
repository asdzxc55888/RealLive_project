from django.urls import path
from .views import indexPage_view

app_name = 'index'

urlpatterns = [
    path('', indexPage_view),
]
