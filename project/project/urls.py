from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
    url(r'^lists/(.+)/$', views.viewList, name='viewList'),
    url(r'^lists/new$', views.newList, name='newList'),
]
