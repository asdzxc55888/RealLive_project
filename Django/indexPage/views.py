from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from livePage.models import UserSetting
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def indexPage_view(request):
    return render(request, 'index.html')

@csrf_exempt
def getStreamer(request):
    streamerList = User.objects.filter(groups__name='Streamer')
    data=[]
    for streamer in streamerList:
        settingData = UserSetting.objects.get(userId=streamer)
        data.append({
            'StreamerName' : settingData.nickName,
            'Introduction' : settingData.introduction,
            'ViewerNumber' : 0,
            'StreamerUserName' : streamer.username
        })
    print(data)
    return JsonResponse(data, safe=False)

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
        settingData.nickName = request.POST.get("nickName")
        settingData.introduction = request.POST.get("introduction")
        settingData.save() #更新進資料庫
    return render(request, 'index.html')
