from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from app.models import Book, ListfOfBooks


def homePage(request):
    return render(request, 'home.html')

def viewList(request, list_of_books_id):
    list_of_books = ListfOfBooks.objects.get(id=list_of_books_id)
    books = Book.objects.filter(list_of_books=list_of_books)

    labels = []
    data = []

    list_of_books_set_for_chart = Book.objects.filter(list_of_books=list_of_books)

    for book in list_of_books_set_for_chart:
        labels.append(book.title)
        percentage = round(book.current_page / book.total_pages * 100, 2)
        data.append(percentage)


    if request.method == 'POST':
        Book.objects.create(title = request.POST['title'],
                            current_page = request.POST['current_page'],
                            total_pages = request.POST['total_pages'],
                            list_of_books = list_of_books,)
        return redirect('/lists/%d/' % (list_of_books.id,))

    return render(request, 'list.html', {'labels': labels,
                                          'data': data,
                                          'list_of_books': list_of_books,
                                          })

def newList(request):
    list_of_books = ListfOfBooks.objects.create()
    book = Book.objects.create(title = request.POST['title'],
                               current_page = request.POST['current_page'],
                               total_pages = request.POST['total_pages'],
                               list_of_books = list_of_books
                               )
    try:
        book.full_clean()
        book.save()
    except ValidationError or ValueError:
        book.delete()
        list_of_books.delete()
        error = 'These fields cannot be blank.'
        return render(request, 'home.html', {"error": error})

    return redirect(f'/lists/{list_of_books.id}/')


def userLogin(request):
    return render(request, '/login.html')


def userLogout(request):
    return render(request, 'logout.html')
