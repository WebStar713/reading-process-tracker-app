from django.shortcuts import render
from app.models import Book

def homePage(request):
    book = Book()
    book.title = request.POST.get('title', '')
    book.current_page = request.POST.get('current_page', 0)
    book.total_pages= request.POST.get('total_pages', 0)
    book.save()

    return render(request, 'home.html',
                    {'new_title': request.POST.get('title', ''),
                     'new_current_page': request.POST.get('current_page', ''),
                     'new_total_pages': request.POST.get('total_pages', ''),
                    })
