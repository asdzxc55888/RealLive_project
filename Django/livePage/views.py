from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from livePage.models import UserSetting

# Create your views here.
def livePage_view(request, streamerName):
    streamer = get_object_or_404(User, username=streamerName)
    streamerSettingData = UserSetting.objects.get(userId=streamer.id)
    context = {
        "youtubeUrl": streamerSettingData.youtubeUrl,
    }
    print(streamer)
    return render(request, 'live.html', context)