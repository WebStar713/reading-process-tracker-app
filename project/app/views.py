from django.shortcuts import render, redirect
from app.models import Book

def homePage(request):

            #### BELOW WORKS TOO ####

    if request.method == 'POST':
        new_title = request.POST['title']
        new_current_page = request.POST['current_page']
        new_total_pages = request.POST['total_pages']

        Book.objects.create(title = new_title,
                            current_page = new_current_page,
                            total_pages = new_total_pages,)
    else:
        new_title = ''
        new_current_page = 0
        new_total_pages = 0

    return render(request, 'home.html', {'new_title' : new_title,
                                         'new_current_page' : new_current_page,
                                         'new_total_pages' : new_total_pages,
                                        })

            #### BELOW WORKS ####

    # if request.method == 'POST':
    #     book = Book()
    #     book.title = request.POST.get('title', '')
    #     book.current_page = request.POST.get('current_page', 0)
    #     book.total_pages = request.POST.get('total_pages', 0)
    #     book.save() # functional_tests pass only when book.save() is commented
    # else:
    #     book = Book()
    #
    # return render(request, 'home.html',
    #                 {'new_title': book.title,
    #                  'new_current_page': book.current_page,
    #                  'new_total_pages': book.total_pages,
    #                 })



    # if request.method == 'POST':
    #     Book.objects.create(title = request.POST['title'],
    #                         current_page = request.POST['current_page'],
    #                         total_pages = request.POST['total_pages'],
    #                         )
    #     return redirect('/')
    #
    # return render(request, 'home.html')
