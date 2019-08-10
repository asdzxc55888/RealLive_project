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

            # calculate interval
            interval = 1
            quantityLimit = [600, 1800, 3600, 7200] # 20 minutes, 1 hours, 2 hours
            intervalList = [3, 6, 12, 24]
            for i in range(len(quantityLimit)):
                if len(emotionData) > quantityLimit[i]:
                    interval = intervalList[i]
                else:
                    break

            # downsize data
            count = 0
            angryDataSum = 0
            disgustDataSum = 0
            fearDataSum = 0
            happyDataSum = 0
            sadDataSum = 0
            surpriseDataSum = 0
            for data in emotionData:
                count += 1
                angryDataSum += data.Angry
                disgustDataSum += data.Disgust
                fearDataSum += data.Fear
                happyDataSum += data.Happy
                sadDataSum += data.Sad
                surpriseDataSum += data.Surprise
                if count == interval:
                    _time.append(data.time.strftime("%H:%M:%S"))
                    _angryData.append(int(angryDataSum / interval))
                    _disgustData.append(int(disgustDataSum / interval))
                    _fearData.append(int(fearDataSum / interval))
                    _happyData.append(int(happyDataSum / interval))
                    _sadData.append(int(sadDataSum / interval))
                    _surpriseData.append(int(surpriseDataSum / interval))
                    count = 0
                    angryDataSum = 0
                    disgustDataSum = 0
                    fearDataSum = 0
                    happyDataSum = 0
                    sadDataSum = 0
                    surpriseDataSum = 0

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
