from django.urls import path
from .views import settingView

app_name = 'setting'

urlpatterns = [
    path('', settingView.as_view()),
]
