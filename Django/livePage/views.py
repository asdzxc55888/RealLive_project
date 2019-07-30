from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from .models import UserSetting

# Create your views here.
class liveView(View):
    template_name = 'live.html'

    def get(self, request, streamerName, *args, **kwargs):
        streamer = get_object_or_404(User, username = streamerName)
        streamerSettingData = UserSetting.objects.get(userId = streamer.id)
        context = {
            "youtubeUrl": streamerSettingData.youtubeUrl,
        }
        print(streamer)
        return render(request, self.template_name, context)
