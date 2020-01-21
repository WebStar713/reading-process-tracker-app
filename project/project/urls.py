from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.homePage, name='home'),
    url(r'^lists/first-list/$', views.viewList, name='viewList'),
]
