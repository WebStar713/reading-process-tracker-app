from django.contrib import admin
from django.conf.urls import url, include

from app import views
from app import urls as app_urls

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', views.homePage, name='homePage'),
    url('', include('app.urls')),
    url(r'^app/', include(app_urls)),
]
