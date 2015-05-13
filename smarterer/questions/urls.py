from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^([0-9]+)/update$', views.update, name='update'),
    url(r'^([0-9]+)/$', views.single, name='single'),
    url(r'^list', views.list, name='list'),
    url(r'^delete', views.delete, name='delete'),
]