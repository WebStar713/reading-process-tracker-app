from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^(\d+)/$', views.viewList, name='viewList'),
    url(r'^(\d+)/add_book$', views.addBook, name='addBook'),
    url(r'^new$', views.newList, name='newList'),
]
