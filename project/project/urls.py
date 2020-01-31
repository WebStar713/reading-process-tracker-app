from django.contrib import admin
from django.conf.urls import url, include

from app import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', views.homePage, name='homePage'),
    url('', include('app.urls')),
]
