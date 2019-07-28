from django.shortcuts import render
from livePage.models import EmotionData

# Create your views here.
def statisticsPage_view(request):
    #obj = EmotionData.objects.get(id = 1)
    content = {
        #'object': obj,
    }
    return render(request, 'statistics.html', content)
