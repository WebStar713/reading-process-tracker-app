from django.conf.urls import url, include

from app import views

urlpatterns = [
    url(r'^$', views.homePage, name='homePage'),
    url(r'^lists/', include('app.urls')),
]
