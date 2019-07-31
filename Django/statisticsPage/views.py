from django.shortcuts import render
from django.views import View
from livePage.models import EmotionData, VideoRecord

# Create your views here.
class statisticsView(View):
    template_name = 'statistics.html'

    def get(self, request, *args, **kwargs):
        _videos = VideoRecord.objects.filter(userId = request.user)
        context = {
            'videos': _videos,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
