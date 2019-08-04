from django.shortcuts import render
from livePage.models import UserSetting

# Create your views here.
def streamerSetting_view(request):
    current_user = request.user
    settingData = UserSetting.objects.get(userId=current_user.id)  # 取得 setting 物件
    context = {
        "youtubeUrl": settingData.youtubeUrl,
        "nickName": settingData.nickName,
        "introduction": settingData.introduction
    }
    return render(request, 'streamerSetting.html', context)

def update(request):
    if request.method == "POST":
        current_user = request.user
        settingData = UserSetting.objects.get(userId=current_user.id)
        settingData.youtubeUrl = request.POST.get("youtubeUrl")
        settingData.nickName = request.POST.get("nickName")
        settingData.introduction = request.POST.get("introduction")
        settingData.save() #更新進資料庫
    return render(request, 'index.html')
