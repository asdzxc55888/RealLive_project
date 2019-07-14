from django.shortcuts import render

# Create your views here.
def indexPage_view(request):
    return render(request, 'index.html')

def streamerSetting_view(request):
    return render(request, 'streamerSetting.html')