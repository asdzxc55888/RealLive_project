from django.shortcuts import render
from django.views import View
from livePage.models import EmotionData

# Create your views here.
class statisticsView(View):
    template_name = 'statistics.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
