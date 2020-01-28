from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from app.models import Book, ListfOfBooks
from app.forms import BookForm


def homePage(request):
    return render(request, 'home.html', {'form': BookForm()})

def viewList(request, list_of_books_id):
    labels = []
    data = []

    list_of_books = ListfOfBooks.objects.get(id=list_of_books_id)
    list_of_books_set_for_chart = Book.objects.filter(list_of_books=list_of_books)

    for book in list_of_books_set_for_chart:
        labels.append(book.title)
        percentage = round(book.current_page / book.total_pages * 100, 2)
        data.append(percentage)

    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST)
        if form.is_valid():
            Book.objects.create(title = request.POST['title'],
                                current_page = request.POST['current_page'],
                                total_pages = request.POST['total_pages'],
                                list_of_books = list_of_books,)
            return redirect(list_of_books)
    return render(request, 'list.html', {'labels': labels,
                                          'data': data,
                                          'list_of_books': list_of_books,
                                          'form': form,
                                          })

def newList(request):
    form = BookForm(data=request.POST)
    if form.is_valid():
        list_of_books = ListfOfBooks.objects.create()
        form.save(for_list=list_of_books)
        return redirect(list_of_books)
    else:
        return render(request, 'home.html', {"form": form})
