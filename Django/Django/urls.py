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
from django.urls import path, re_path
from livePage.views import livePage_view, login, logout, register
from indexPage.views import indexPage_view, streamerSetting_view, updata
from statisticsPage.views import statisticsPage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/',login),
    path('accounts/logout/',logout),
    path('accounts/register/',register),
    path('live/<userAccount>', livePage_view),
    path('', indexPage_view),
    path('setting/', streamerSetting_view),
    path('statistics/', statisticsPage_view),
    path('setting/updata', updata)
]
