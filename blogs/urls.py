# -*- coding: utf-8 -*-

from django.conf.urls import url
from .views import MainView, AccountView, ErrorView, MyBlogView, AddEntryView, AllBlogsView, BlogPageView
from .views import subscription, unsubscription
from .views import logout_view

urlpatterns = [
	url(r'^$', MainView.as_view(), name='index'),
	url(r'^account/$', AccountView.as_view(), name='account'),
	url(r'^account/error/$', ErrorView.as_view(template_name='error_login.html'), name='login_error'),
	url(r'^account/logout/$', logout_view, name='logout'),

	url(r'^account/my_blog/$', MyBlogView.as_view(), name='my_blog'),
	url(r'^account/my_blog/add_entry/$', AddEntryView.as_view(), name='add_entry'),
	url(
		r'^account/my_blog/add_entry/error/$',
		ErrorView.as_view(template_name='error_add_entry.html'),
		name='add_entry_error'
	),

	url(r'^account/all_blogs/$', AllBlogsView.as_view(), name='all_blogs'),
	url(r'^account/subscription/(?P<pk>\d+)/$', subscription, name='subscription'),
	url(r'^account/unsubscription/(?P<pk>\d+)/$', unsubscription, name='unsubscription'),
	url(r'^account/blog/(?P<pk>\d+)/$', BlogPageView.as_view(), name='blog_page'),

]