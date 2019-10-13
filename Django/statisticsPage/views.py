from django.shortcuts import render
from django.views import View
from livePage.models import UserSetting, EmotionData, VideoRecord, ChatRecord
from django.http import JsonResponse
from django.contrib.auth.models import User
from livePage.models import UserSetting
import json

# Create your views here.
class statisticsView(View):
    template_name = 'statistics.html'

    def get(self, request, streamerName, *args, **kwargs):
        _user = User.objects.get(username = streamerName)
        _userSetting = UserSetting.objects.get(userId = _user, isLive = True)
        _videos = VideoRecord.objects.filter(userId = _user).exclude(vid = _userSetting.youtubeUrl)

        context = {
            'videos': _videos,
        }
        return render(request, self.template_name, context)

    def post(self, request, streamerName, *args, **kwargs):
        # get videos
        _user = User.objects.get(username = streamerName)
        _userSetting = UserSetting.objects.get(userId = _user, isLive = True)
        _videos = VideoRecord.objects.filter(userId = _user).exclude(vid = _userSetting.youtubeUrl)

        _vid = request.POST.get("vid", "")
        video = VideoRecord.objects.get(vid = _vid)

        context = {
            'videos': _videos,
            'vid': _vid
        }

        if request.user.is_authenticated:
            _time = []
            _angryData = []
            _disgustData = []
            _fearData =[]
            _happyData = []
            _sadData = []
            _surpriseData = []

            # get emotional data
            emotionData = EmotionData.objects.filter(vid = video)

            # calculate hours
            hours = int(len(emotionData) / 3600);
            if len(emotionData) % 3600 > 0:
                hours += 1

            for data in emotionData:
                _time.append(data.time.strftime("%H:%M:%S"))
                _angryData.append(int(data.Angry))
                _disgustData.append(int(data.Disgust))
                _fearData.append(int(data.Fear))
                _happyData.append(int(data.Happy))
                _sadData.append(int(data.Sad))
                _surpriseData.append(int(data.Surprise))

            context['time'] = json.dumps(_time)
            context['angryData'] = _angryData
            context['disgustData'] = _disgustData
            context['fearData'] = _fearData
            context['happyData'] = _happyData
            context['sadData'] = _sadData
            context['surpriseData'] = _surpriseData
            context['hours'] = hours

        return render(request, self.template_name, context)


def getChatRecord(request):
    _vid = request.POST.get("vid", "")
    _videoRecord = VideoRecord.objects.get(vid = _vid)
    _chatRecord = ChatRecord.objects.filter(vid = _videoRecord).order_by('nDate', 'nTime')
    rtnMessage = []

    for chatRecord in _chatRecord.all():
        user = User.objects.get(username = chatRecord.userId)
        userSetting = UserSetting.objects.get(userId = user)
        rtnMessage.append(userSetting.nickName + ":" + chatRecord.message)

    return JsonResponse(rtnMessage, safe=False)
