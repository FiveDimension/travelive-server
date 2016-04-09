#coding: utf-8
from django.conf.urls import patterns, include, url
from dashboard import views

urlpatterns = patterns('',
    url(r'^$', 'dashboard.views.index'),
    url(r'^searchVp$', 'dashboard.views.searchVp'),
    url(r'^simpleSearchVp$', 'dashboard.views.simpleSearchVp'),
    url(r'^getVpDetail$', 'dashboard.views.getVpDetail'),
    url(r'^createStream$', 'dashboard.views.createStream'),
    url(r'^getStream$', 'dashboard.views.getStream'),
    url(r'^getStreamList$', 'dashboard.views.getStreamList'),
    url(r'^deleteStream$', 'dashboard.views.deleteStream'),
    url(r'^doFavorite$', 'dashboard.views.doFavorite'),
    url(r'^addUser$', 'dashboard.views.addUser'),
    url(r'^login$', 'dashboard.views.login'),
    # url(r'^property/$', views.propertyList.as_view()),
)