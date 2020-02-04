from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from app.models import Book, ListfOfBooks
from app.forms import BookForm, ExisitingBooksInList


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

    form = ExisitingBooksInList(for_list = list_of_books, owner=request.user)
    if request.method == 'POST':
        form = ExisitingBooksInList(for_list = list_of_books, owner=request.user, data=request.POST)
        if form.is_valid():
            print(form.owner)
            print(request.user)
            form = None
            form = BookForm(data=request.POST)
            form = form.save(for_list=list_of_books)
            form.owner = request.user
            form.save()
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
        form = form.save(for_list=list_of_books)
        form.owner = request.user
        form.list_of_books = list_of_books
        form = form.save()
        return redirect(list_of_books)
    else:
        return render(request, 'home.html', {"form": form})

def myList(request):

    list_of_books_set_for_chart = Book.objects.filter(owner = request.user)

    books_set_ID = []
    list_of_books_set_ID = []
    for i in list_of_books_set_for_chart:
        books_set_ID.append(i.id)
        list_of_books_set_ID.append(i.list_of_books_id)

    labels = []
    data = []

    if list_of_books_set_ID != []:

        for book in list_of_books_set_for_chart:
            labels.append(book.title)
            percentage = round(book.current_page / book.total_pages * 100, 2)
            data.append(percentage)

        list_of_books = ListfOfBooks.objects.get(id=list_of_books_set_ID[0])
        form = ExisitingBooksInList(for_list = list_of_books, owner=request.user)
        if request.method == 'POST':
            form = ExisitingBooksInList(for_list = list_of_books, owner=request.user, data=request.POST)
            if form.is_valid():
                print(form.owner)
                print(request.user)
                form = None
                form = BookForm(data=request.POST)
                form = form.save(for_list=list_of_books)
                form.owner = request.user
                form.save()
                return redirect(list_of_books)
        form = ExisitingBooksInList(for_list = list_of_books, owner=request.user)

        return render(request, 'myList.html', {'labels': labels,
                                              'data': data,
                                              'list_of_books': list_of_books,
                                              'form': form,
                                              })
    else:
        return render(request, 'home.html', {'form': BookForm()})

def register(request):
    return render(request, 'register.html')
