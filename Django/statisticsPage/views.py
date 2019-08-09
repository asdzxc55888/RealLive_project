from django.shortcuts import render
from django.views import View
from livePage.models import EmotionData, VideoRecord
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
            for data in emotionData:
                _time.append(data.time.strftime("%H:%M:%S"))
                _angryData.append(data.Angry)
                _disgustData.append(data.Disgust)
                _fearData.append(data.Fear)
                _happyData.append(data.Happy)
                _sadData.append(data.Sad)
                _surpriseData.append(data.Surprise)

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
        }
        return render(request, self.template_name, context)
