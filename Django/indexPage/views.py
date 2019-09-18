from django.shortcuts import render,render_to_response
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from indexPage.form import UserCreationForm
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from livePage.models import UserSetting
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import json
import random
import string

# Create your views here.
class indexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@csrf_exempt
def getStreamer(request):
    streamerList = User.objects.filter(groups__name='Streamer')
    data=[]
    for streamer in streamerList:
        settingData = UserSetting.objects.get(userId=streamer)
        if settingData.isLive:
            data.append({
                'StreamerUserName' : streamer.username, 
                'StreamerName' : settingData.nickName + ' (' + streamer.username + ')',
                'Category' : settingData.category,
                'Introduction' : settingData.introduction,
            })
        #print(data)
    return JsonResponse(data, safe=False)

#登入
def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    username = request.POST.get('uname', '') #取得參數
    password = request.POST.get('psw', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        rtnMessage = {
            'success': True,
            'messages': "登入成功！"
        }
    else:
        rtnMessage = {
            'success': False,
            'messages': "登入失敗,請確認帳號密碼是否正確！"
        }

    return JsonResponse(rtnMessage, safe=False)

#登出
def logout(request):
    auth.logout(request)
    rtnMessage = {
        'success': True
    }
    return JsonResponse(rtnMessage, safe=False)

#註冊
def register(request):
    if request.method == 'POST':
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                rtnMessage = {
                    'success': True,
                    'messages': "創建帳號成功！"
                }
                UserSetting.objects.create(userId = user, nickName = user.username) #建立使用者設定資料
            else:
                rtnMessage = {
                    'success': False,
                    'messages': form.errors
                }
        except ValidationError as err:
            rtnMessage = {
                'success': False,
                'messages': err.messages
            }

    return JsonResponse(rtnMessage, safe=False)

#忘記密碼
def forgotPassword(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get("username_forgot"))
        except ValidationError as err:
            rtnMessage = {
                'success': False,
                'messages': "查無此使用者,請檢查輸入"
            }

        userSetting = UserSetting.objects.create(userId = user)
        newPassword = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))

        #設定亂數新密碼
        user.set_password(newPassword)
        user.save()

        #mail init setting
        emailMessage = 'Your new password is ' + newPassword

        if settings.EMAIL_TEST: #test mode
            send_mail('Realive System forgot password', emailMessage, settings.DEFAULT_FROM_EMAIL,
                [settings.TEST_EMAIL_TO], fail_silently=False)
        else:
            send_mail('Realive System forgot password', emailMessage, settings.DEFAULT_FROM_EMAIL,
                [user.email], fail_silently=False)

        rtnMessage = {
            'success': True,
            'messages': "成功寄發信件,請至郵箱中查閱！"
        }

        return JsonResponse(rtnMessage, safe=False)
