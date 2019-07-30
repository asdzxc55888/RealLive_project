from django.urls import path
from .views import statisticsView

app_name = 'statistics'

urlpatterns = [
    path('', statisticsView.as_view()),
]
