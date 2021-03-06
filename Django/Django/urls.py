"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from indexPage.views import getStreamer, login, logout, register, resetPassword, SendVerificationCode

urlpatterns = [
    path('', include('indexPage.urls')),
    path('live/', include('livePage.urls')),
    path('liveSetting/', include('liveSettingPage.urls')),
    path('statistics/', include('statisticsPage.urls')),
    path('setting/', include('settingPage.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', login),
    path('accounts/logout/', logout),
    path('accounts/register/', register),
    path('accounts/resetPassword/<encodeUsername>/', resetPassword),
    path('accounts/SendVerificationCode/', SendVerificationCode),
    path('getStreamer', getStreamer)
]
