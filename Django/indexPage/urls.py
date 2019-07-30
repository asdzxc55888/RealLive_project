from django.urls import path
from .views import indexView

app_name = 'index'

urlpatterns = [
    path('', indexView.as_view()),
]
