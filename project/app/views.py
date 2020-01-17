from django.shortcuts import render

def homePage(request):
    return render(request, 'home.html',
                    {'new_title': request.POST.get('title', ''),
                     'new_current_page': request.POST.get('current_page', ''),
                     'new_total_pages': request.POST.get('total_pages', ''),
                    })
