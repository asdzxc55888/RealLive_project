from django.shortcuts import render
from django.views import View
from livePage.models import EmotionData, VideoRecord, ChatRecord
from django.http import JsonResponse
from django.contrib.auth.models import User
from livePage.models import UserSetting
import json

# Create your views here.
class statisticsView(View):
    template_name = 'statistics.html'

    def get(self, request, *args, **kwargs):
        _videos = None
        if request.user.is_authenticated:
            _videos = VideoRecord.objects.filter(userId = request.user)
        context = {
            'videos': _videos,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        _videos = None
        _vid = request.POST.get("vid", "")
        _time = []
        _angryData = []
        _disgustData = []
        _fearData =[]
        _happyData = []
        _sadData = []
        _surpriseData = []
        if request.user.is_authenticated:
            # get videos
            _videos = VideoRecord.objects.filter(userId = request.user)

            # get emotional data
            video = VideoRecord.objects.get(vid = _vid)
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

        context = {
            'videos': _videos,
            'vid': _vid,
            'time': json.dumps(_time),
            'angryData': _angryData,
            'disgustData': _disgustData,
            'fearData': _fearData,
            'happyData': _happyData,
            'sadData': _sadData,
            'surpriseData': _surpriseData,
            'hours': hours,
        }
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
