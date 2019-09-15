from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from livePage.models import UserSetting
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, password_changed
from django.core.exceptions import ValidationError
import json

# Create your views here.
class settingView(View):
    template_name = 'setting.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        print(current_user)
        #判斷是否登入
        if not current_user.is_anonymous:
            settingData = UserSetting.objects.get(userId=current_user.id)  # 取得 setting 物件
            if request.user.is_authenticated:
                context = {
                "email": current_user.email,
                "nickName": settingData.nickName,
                "youtubeUrl": settingData.youtubeUrl,
                "introduction": settingData.introduction,
                "isStreamer": 'True',
                }
            else:
                context = {
                "email": current_user.email,
                "nickName": settingData.nickName,
                "youtubeUrl": '',
                "introduction": '',
                "isStreamer": 'False',
                }

            return render(request, self.template_name, context)
        else:
            return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        current_user = request.user
        settingData = UserSetting.objects.get(userId=current_user.id)
        current_user.email = request.POST.get("email")
        settingData.nickName = request.POST.get("nickName")
        settingData.save() #更新進資料庫
        return render(request, 'setting.html')

class streamSettingView(View):
    template_name = 'setting.html'

    def post(self, request, *args, **kwargs):
        current_user = request.user
        print( request.POST.get("introduction"))
        settingData = UserSetting.objects.get(userId=current_user.id)
        settingData.youtubeUrl = request.POST.get("youtubeUrl")
        settingData.introduction = request.POST.get("introduction")
        settingData.save() #更新進資料庫
        return render(request, 'setting.html')

class modifyPasswordView(View):
        template_name = 'modifyPassword.html'

        def get(self, request, *args, **kwargs):
            return render(request, self.template_name)

        def post(self, request, *args, **kwargs):
            user = User.objects.get(id=request.user.id)
            print(user)
            status = False

            #判斷是否成功 設定傳送訊息
            if user.check_password(request.POST.get("oldPassword")):

                if request.POST.get("newPassword1")==request.POST.get("newPassword2"):
                    try:
                        validate_password(request.POST.get("newPassword1"), user)
                        user.set_password(request.POST.get("newPassword1"))
                        user.save()
                        passwordValidate = "修改成功"
                        status = True
                    except ValidationError as err:
                        passwordValidate = err.messages
                else:
                    passwordValidate = "請確認密碼是否輸入相同"

            else:
                passwordValidate = "密碼錯誤"
            context = {
                "status":status,
                "passwordValidate":passwordValidate[0], #get array first
            }
            j_context = json.dumps(context)
            return HttpResponse(j_context)
