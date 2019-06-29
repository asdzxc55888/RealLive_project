from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template import RequestContext

# Create your views here.
def livePage_view(request):
    return render(request, 'live.html')

########################### 登入註冊 #########################################
def login(request):

    if request.user.is_authenticated: 
        return HttpResponseRedirect('/')

    username = request.POST.get('uname', '')
    password = request.POST.get('psw', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        messages.warning(request, 'Your password has been changed successfully!', extra_tags='alert')
        return render(request, 'live.html')

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