from django.urls import path
from .views import statisticsPage_view

app_name = 'statistics'

urlpatterns = [
    path('', statisticsPage_view),
]
