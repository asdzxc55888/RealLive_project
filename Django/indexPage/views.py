from django.shortcuts import render,render_to_response
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from livePage.models import UserSetting
from django.core.exceptions import ValidationError
import json

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
        data.append({
            'StreamerName' : settingData.nickName,
            'Introduction' : settingData.introduction,
            'ViewerNumber' : 0,
            'StreamerUserName' : streamer.username
        })
    print(data)
    return JsonResponse(data, safe=False)

#登入
def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    username = request.POST.get('uname', '') #取得參數
    password = request.POST.get('psw', '')

    user = auth.authenticate(username=username, password=password) #取得參數

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        messages.warning(request, 'Your password has been changed successfully!', extra_tags='alert')
        return HttpResponseRedirect('/')

#登出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

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
def forgetPassword(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get("userName"))
