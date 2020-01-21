from django.shortcuts import render, redirect
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
    


    return render(request, 'list.html', {'labels': labels,
                                          'data': data,
                                          'list_of_books': list_of_books,
                                          })

def newList(request):
    list_of_books = ListfOfBooks.objects.create()
    Book.objects.create(title = request.POST['title'],
                        current_page = request.POST['current_page'],
                        total_pages = request.POST['total_pages'],
                        list_of_books = list_of_books
                        )
    return redirect(f'/lists/{list_of_books.id}/')

def addBook(request, list_of_books_id):
    list_of_books = ListfOfBooks.objects.get(id=list_of_books_id)
    Book.objects.create(title = request.POST['title'],
                        current_page = request.POST['current_page'],
                        total_pages = request.POST['total_pages'],
                        list_of_books = list_of_books
                        )
    return redirect(f'/lists/{list_of_books.id}/')

# def chart(request, list_of_books_id):
#     labels = []
#     data = []
#
#     list_of_books = ListfOfBooks.objects.get(id=list_of_books_id)
#     list_of_books_set_for_chart = Book.objects.filter(list_of_books=list_of_books)
#     for book in list_of_books_set_for_chart:
#         labels.append(book.title)
#         percentage = round(book.current_page / book.total_pages * 100, 2)
#         data.append(percentage)
#
#     return render(request, 'chart.html', {'labels': labels,
#                                           'data': data,
#                                           })
