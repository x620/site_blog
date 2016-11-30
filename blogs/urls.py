# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import MainView, LoginErrorView, AccountView
from .views import logout_view

urlpatterns = [
	url(r'^$', MainView.as_view(), name='index'),
	url(r'^account/$', AccountView.as_view(), name='account'),
	url(r'^account/error/$', LoginErrorView.as_view(), name='login_error'),
	url(r'^account/logout/$', logout_view, name='logout'),
]