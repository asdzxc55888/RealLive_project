from django.shortcuts import render

# Create your views here.
def statisticsPage_view(request):
    return render(request, 'statistics.html')
