from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from livePage.models import UserSetting
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, password_changed
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
import json

# Create your views here.
class settingView(View):
    template_name = 'setting.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user

        #判斷是否登入
        if not current_user.is_anonymous:
            settingData = UserSetting.objects.get(userId=current_user.id)  # 取得 setting 物件
            if current_user.groups.filter(name = 'Streamer').exists():
                context = {
                "email": current_user.email,
                "nickName": settingData.nickName,
                "youtubeUrl": settingData.youtubeUrl,
                "introduction": settingData.introduction,
                "isStreamer": True,
                }
            else:
                context = {
                "email": current_user.email,
                "nickName": settingData.nickName,
                "youtubeUrl": '',
                "introduction": '',
                "isStreamer": False,
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
        #return render(request, 'setting.html')

        rtnMessage = {
            'success': True,
            'messages': "修改成功！"
        }
        return JsonResponse(rtnMessage, safe=False)

class streamSettingView(View):
    template_name = 'setting.html'

    def post(self, request, *args, **kwargs):
        current_user = request.user
        settingData = UserSetting.objects.get(userId=current_user.id)
        settingData.youtubeUrl = request.POST.get("youtubeUrl")
        settingData.category = request.POST.get("category")
        settingData.introduction = request.POST.get("introduction")
        settingData.save() #更新進資料庫
        #return render(request, 'setting.html')
        rtnMessage = {
            'success': True,
            'messages': "修改成功！"
        }
        return JsonResponse(rtnMessage, safe=False)

def BecomeStreamer(request):
    if request.method == 'POST':
        try:
            streamerGroup = Group.objects.get(name='Streamer')
            streamerGroup.user_set.add(request.user)
            rtnMessage = {
                'success': True,
                'messages': '申請實況主成功！'
            }
        except ValidationError as err:
            rtnMessage = {
                'success': False,
                'messages': err.message
            }

        return JsonResponse(rtnMessage, safe=False)

class modifyPasswordView(View):
        template_name = 'modifyPassword.html'

        def get(self, request, *args, **kwargs):
            return render(request, self.template_name)

        def post(self, request, *args, **kwargs):
            user = User.objects.get(id=request.user.id)
            status = False
            passwordValidate=[]
            #判斷是否成功 設定傳送訊息
            if user.check_password(request.POST.get("oldPassword")):

                if request.POST.get("newPassword1")==request.POST.get("newPassword2"):
                    try:
                        validate_password(request.POST.get("newPassword1"), user)
                        user.set_password(request.POST.get("newPassword1"))
                        user.save()
                        passwordValidate.append("修改成功")
                        status = True
                    except ValidationError as err:
                        passwordValidate = err.messages
                else:
                    passwordValidate.append("請確認密碼是否輸入相同")

            else:
                passwordValidate.append("密碼錯誤")
            context = {
                "status":status,
                "passwordValidate":passwordValidate[0], #get array first
            }
            j_context = json.dumps(context)
            return HttpResponse(j_context)
