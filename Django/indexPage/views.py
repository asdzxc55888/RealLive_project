from django.shortcuts import render,render_to_response
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from indexPage.form import UserCreationForm
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from livePage.models import UserSetting, VideoRecord
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from .cryptSet import prpcrypt
from django.utils.html import strip_tags
import json
import random
import string

resetPasswordKey = 'abcdef'  # 金鑰 8位或16位,必須為bytes

# Create your views here.
class indexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@csrf_exempt
def getStreamer(request):
    searchFilter = request.POST.get("searchFilter")
    #搜尋結果
    if searchFilter is not None:
        nickNameFilterList = UserSetting.objects.filter(nickName__contains = searchFilter)
        userNameFilterList = User.objects.filter(username__contains = searchFilter)
        searchResult = userNameFilterList
        for nickNameFilter in nickNameFilterList:
            instance = User.objects.get(username=nickNameFilter.userId)
            searchResult |= User.objects.filter(pk=instance.pk)

        streamerList = searchResult.filter(groups__name='Streamer')
    else:
        streamerList = User.objects.filter(groups__name='Streamer')

    data=[]

    #取得當前直播的實況主
    for streamer in streamerList:
        settingData = UserSetting.objects.get(userId=streamer)
        if settingData.isLive:
            data.append({
                'vid': settingData.youtubeUrl,
                'StreamerUserName' : streamer.username,
                'StreamerName' : settingData.nickName + ' (' + streamer.username + ')',
                'Category' : settingData.category,
                'Introduction' : settingData.introduction,
            })

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
def resetPassword(request, encodeUsername):
    if request.method == 'GET':
        try:
            pc = prpcrypt(resetPasswordKey)  # 初始化金鑰
            username = pc.decrypt(encodeUsername)
            user = User.objects.get(username=username)
            print(username)
        except ValidationError as err:
            context = {
                "message" :"System error!"
            }

            return render(request, "resetPassword.html", context)

        newPassword = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))

        #設定亂數新密碼
        user.set_password(newPassword)
        user.save()

        #mail init setting
        serverHost = 'realive.online'

        url = 'https://' + serverHost + '/'
        html_message = 'This is your new password [' + newPassword + '] please enter the Realive web to change your password <br/> <a href=' + url + '>' + url + '</a>'
        plain_message = strip_tags(html_message)

        if settings.EMAIL_TEST: #test mode
            to = settings.TEST_EMAIL_TO
        else:
            to = user.email

        send_mail('Reset your password', plain_message, settings.DEFAULT_FROM_EMAIL,
            [to], html_message=html_message)

        context = {
            "message" :"Success Change new Password! Please check your email to get the new password."
        }

        return render(request, "resetPassword.html", context)


def SendVerificationCode(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST.get("username_forgot"))
        except ValidationError as err:
            rtnMessage = {
                'success': False,
                'messages': "查無此使用者,請檢查輸入"
            }

        #encode
        pc = prpcrypt(resetPasswordKey)  # 初始化金鑰
        encodeUsername = pc.encrypt(user.username)

        #mail init setting
        serverHost = '127.0.0.1:8000'

        url = 'https://' + serverHost + '/accounts/resetPassword/' + encodeUsername.decode('utf-8')
        html_message = 'click this <a href=' + url + '>link</a> to reset your password <br/> ' + '<a href=' + url + '>' + url + '</a>'
        plain_message = strip_tags(html_message)

        if settings.EMAIL_TEST: #test mode
            to = settings.TEST_EMAIL_TO
        else:
            to = user.email

        send_mail('Reset your password', plain_message, settings.DEFAULT_FROM_EMAIL,
            [to], html_message=html_message)

        rtnMessage = {
            'success': True,
            'messages': "成功寄發驗證信,請至郵箱中查閱！"
        }

        return JsonResponse(rtnMessage, safe=False)

def pad(text):
    """
    # 加密函式，如果text不是8的倍數【加密文字text必須為8的倍數！】，那就補足為8的倍數
    :param text:
    :return:
    """
    while len(text) % 8 != 0:
        text += ' '
    return text
