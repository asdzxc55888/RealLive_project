from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from livePage.models import UserSetting
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

########################### 登入註冊 #########################################
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

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()   # 將user資料寫入資料庫
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html',locals())
########################### !登入註冊 ######################################
