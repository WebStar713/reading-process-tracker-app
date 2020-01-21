from django.shortcuts import render, redirect
from app.models import Book

def homePage(request):
    if request.method == 'POST':
        Book.objects.create(title = request.POST['title'],
                            current_page = request.POST['current_page'],
                            total_pages = request.POST['total_pages'],
                            )
        return redirect('/lists/first-list/')

    return render(request, 'home.html')

def viewList(request):
    books = Book.objects.all()
    return render(request, 'list.html', {'books': books})
