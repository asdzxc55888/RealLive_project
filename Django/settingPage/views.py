from django.shortcuts import render
from django.views import View
from livePage.models import UserSetting

# Create your views here.
class settingView(View):
    template_name = 'streamerSetting.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        if request.user.is_authenticated:
            settingData = UserSetting.objects.get(userId=current_user.id)  # 取得 setting 物件
            context = {
                "youtubeUrl": settingData.youtubeUrl,
                "nickName": settingData.nickName,
                "introduction": settingData.introduction,
                "isStreamer": 'True'
            }
        else:
            context = {
                "youtubeUrl": '',
                "nickName": '',
                "introduction": '',
                "isStreamer": 'False'
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        settingData = UserSetting.objects.get(userId=current_user.id)
        settingData.youtubeUrl = request.POST.get("youtubeUrl")
        settingData.nickName = request.POST.get("nickName")
        settingData.introduction = request.POST.get("introduction")
        settingData.save() #更新進資料庫
        return render(request, 'index.html')
