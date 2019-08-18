from django.urls import path
from .views import settingView, modifyPasswordView

app_name = 'setting'

urlpatterns = [
    path('', settingView.as_view()),
    path('modifyPassword', modifyPasswordView.as_view()),
]
