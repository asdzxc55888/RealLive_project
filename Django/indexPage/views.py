from django.shortcuts import render
from django.contrib.auth.models import User
from livePage.models import UserSetting
import json

# Create your views here.


def indexPage_view(request):
    return render(request, 'index.html')


def streamerSetting_view(request):
    current_user = request.user
    settingData = UserSetting.objects.get(userId=current_user.id)  # 取得 setting 物件
    context = {
        "youtubeUrl": settingData.youtubeUrl,
        "nickName": settingData.nickName,
        "introduction": settingData.introduction
    }
    return render(request, 'streamerSetting.html', context)


def updata(request):
    if request.method == "POST":
        current_user = request.user
        settingData = UserSetting.objects.get(userId=current_user.id)
        settingData.youtubeUrl = request.POST.get("youtubeUrl")
        settingData.save() #更新進資料庫
        print(request.POST.get("nickName"))
        print(request.POST.get("introduction"))
    return render(request, 'streamerSetting.html')
