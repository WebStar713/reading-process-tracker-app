from django.shortcuts import render
from django.http import HttpResponse

def homePage(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['title'])
    return render(request, 'home.html')
