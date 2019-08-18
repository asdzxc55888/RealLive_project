from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from livePage.models import UserSetting
from django.contrib.auth.models import User
import json

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

class modifyPasswordView(View):
        template_name = 'modifyPassword.html'

        def get(self, request, *args, **kwargs):
            return render(request, self.template_name)

        def post(self, request, *args, **kwargs):
            user = User.objects.get(id=request.user)
            print(user)
            if user.check_password(request.POST.get("newPassword1")):

                if request.POST.get("newPassword1")==request.POST.get("newPassword2"):
                    user.set_password(request.POST.get("newPassword1"))
                    message = "修改成功"
                else:
                    message = "請確認密碼是否輸入相同"

            else:
                message = "密碼錯誤"

            context = {
                "message":message,
            }
            print(message)
            return render(request, self.template_name, context)
