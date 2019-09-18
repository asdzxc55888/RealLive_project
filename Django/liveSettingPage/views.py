from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from livePage.models import UserSetting, VideoRecord, EmotionData

# Create your views here.
class liveSettingView(View):
    template_name = 'liveSetting.html'

    def get(self, request, streamerName, *args, **kwargs):
        streamer = get_object_or_404(User, username = streamerName)
        settingData = UserSetting.objects.get(userId = streamer)
        context = {
            "streamerName": streamerName,
            "youtubeUrl": settingData.youtubeUrl,
            "introduction": settingData.introduction,
            "isLive": settingData.isLive,
            "message": ' ',
        }
        return render(request, self.template_name, context)

    def post(self, request, streamerName, *args, **kwargs):
        settingData = UserSetting.objects.get(userId = request.user.id)
        if request.POST.get("state") == '1' and VideoRecord.objects.filter(vid = request.POST.get("youtubeUrl")).exists():
            message = "The Youtube vid is duplicate."
        elif request.POST.get("state") == '0' and not settingData.isLive:
            message = "Live was already closed."
        else:
            settingData.youtubeUrl = request.POST.get("youtubeUrl")
            settingData.introduction = request.POST.get("introduction")
            if request.POST.get("state") == '0':
                settingData.isLive = False
                message = "Successfully closed."
            elif request.POST.get("state") == '1':
                VideoRecord.objects.create(userId = request.user, vid = settingData.youtubeUrl)
                settingData.isLive = True
                message = "Successfully opened."
            elif request.POST.get("state") == '2':
                message = "Successfully modified."
            settingData.save()
        context = {
            "streamerName": streamerName,
            "youtubeUrl": settingData.youtubeUrl,
            "introduction": settingData.introduction,
            "isLive": settingData.isLive,
            "message": message,
        }
        return render(request, self.template_name, context)

def updateEmotionData(request, streamerName, *args, **kwargs):
    video = VideoRecord.objects.get(userId = request.user, vid = request.POST.get("vid"))
    happy = '0'
    surprised = '0'
    if EmotionData.objects.filter(vid = video).exists():
        data = EmotionData.objects.filter(vid = video).latest('id')
        happy = data.Happy
        surprised = data.Surprise
    return JsonResponse({
        'status': 'ok',
        'happy': happy,
        'surprised': surprised,
    })
