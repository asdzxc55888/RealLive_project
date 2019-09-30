from django.urls import path
from .views import statisticsView, getChatRecord

app_name = 'statistics'

urlpatterns = [
    path('', statisticsView.as_view()),
    path('getChatRecord', getChatRecord),
]
