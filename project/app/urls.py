from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth import views as auth_views

from app import views

urlpatterns = [
    url(r'^lists/(\d+)/$', views.viewList, name='viewList'),
    url(r'^lists/new$', views.newList, name='newList'),
    url(r'^mylist/$', views.myList, name='myList'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.bookDelete, name='bookDelete'),

    path('', auth_views.LoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
