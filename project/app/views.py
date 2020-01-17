from django.shortcuts import render

def homePage(request):
    return render(request, 'home.html', {'new_title': request.POST.get('title', ''),})
