from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^lists/(\d+)/$', views.viewList, name='viewList'),
    url(r'^lists/(\d+)/add_book$', views.addBook, name='addBook'),
    url(r'^lists/new$', views.newList, name='newList'),
    url(r'^login/$', views.userLogin, name='userLogin'),
]
