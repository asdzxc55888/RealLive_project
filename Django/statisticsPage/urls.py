from django.urls import path
from .views import statisticsView, getChatRecord

app_name = 'statistics'

urlpatterns = [
    path('<username>', statisticsView.as_view()),
    path('get/getChatRecord', getChatRecord),
]
