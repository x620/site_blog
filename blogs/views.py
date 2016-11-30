# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from forms import LoginForm, AddEntryForm
from .models import Blog, Entry, Subscription

import logging
logger = logging.getLogger(__name__)


# Register and Authorization
class MainView(FormView):
	template_name = 'main.html'
	form_class = LoginForm
	success_url = reverse_lazy('account')

	def form_valid(self, form):
		if self.request.method == 'POST':
			send_form = LoginForm(self.request.POST)
			if send_form.is_valid():
				# Получение данных из формы
				username = send_form.cleaned_data['username']
				password = send_form.cleaned_data['password']

				user = authenticate(username=username, password=password)
				if user is not None:
					login(self.request, user)
					# Редирект на страницу "Аккаунт"
					return super(MainView, self).form_valid(form)
			return redirect('login_error')

	def get_context_data(self, **kwargs):
		context = super(MainView, self).get_context_data(**kwargs)
		context['login_form'] = self.form_class
		context['main'] = True
		return context


class ErrorView(TemplateView):
	pass


def logout_view(request):
	logout(request)
	return redirect('index')


class AccountView(LoginRequiredMixin, TemplateView):
	login_url = reverse_lazy('index')
	template_name = 'account.html'

	def get_context_data(self, **kwargs):
		context = super(AccountView, self).get_context_data(**kwargs)
		context['main'] = True
		return context


class MyBlogView(LoginRequiredMixin, ListView):
	template_name = 'blog_page.html'
	context_object_name = 'entries_list'

	def get_queryset(self):
		return Entry.objects.filter(blog__user=self.request.user).order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(MyBlogView, self).get_context_data(**kwargs)
		context['my_blog'] = True
		return context


class AddEntryView(LoginRequiredMixin, FormView):
	template_name = 'add_entry.html'
	form_class = AddEntryForm
	success_url = reverse_lazy('my_blog')

	def form_valid(self, form):
		if self.request.method == 'POST':
			add_entry_form = AddEntryForm(self.request.POST)
			if add_entry_form.is_valid():
				title = add_entry_form.cleaned_data['title']
				body = add_entry_form.cleaned_data['body']

				blog = Blog.objects.get(user=self.request.user)
				entry = Entry(blog=blog, body=body)
				entry.title = title
				entry.save()

				return super(AddEntryView, self).form_valid(form)
			else:
				return redirect('add_entry_error')

	def get_context_data(self, **kwargs):
		context = super(AddEntryView, self).get_context_data(**kwargs)
		context['add_entry_form'] = self.form_class
		return context


class AllBlogsView(LoginRequiredMixin, ListView):
	template_name = 'all_blogs.html'
	model = Blog

	def get_context_data(self, **kwargs):
		all_blogs = Blog.objects.exclude(user=self.request.user)
		subs = Subscription.objects.filter(user=self.request.user)

		unsubs_blog_list = [sub.blog for sub in subs]
		subs_blog_list = [blog for blog in all_blogs if blog not in unsubs_blog_list]

		context = super(AllBlogsView, self).get_context_data(**kwargs)
		context['subs_blog_list'] = subs_blog_list
		context['unsubs_blog_list'] = unsubs_blog_list
		return context


class BlogPageView(LoginRequiredMixin, ListView):
	template_name = 'blog_page.html'
	context_object_name = 'entries_list'

	def get_queryset(self):
		return Entry.objects.filter(blog_id=int(self.kwargs['pk'])).order_by('-pub_date')

	def get_context_data(self, **kwargs):
		context = super(BlogPageView, self).get_context_data(**kwargs)
		context['blog'] = Blog.objects.get(id=int(self.kwargs['pk']))
		return context


def subscription(request, pk):
	blog = get_object_or_404(Blog, pk=int(pk))
	logger.debug('Blog: %s' % blog)
	new_subscription = Subscription(user=request.user, blog=blog)
	new_subscription.save()
	logger.debug('Subscription saved.')
	return redirect('all_blogs')


def unsubscription(request, pk):
	blog = get_object_or_404(Blog, pk=int(pk))
	logger.debug('Blog: %s' % blog)
	subscriptions = Subscription.objects.filter(user=request.user, blog=blog)
	subscriptions.delete()
	logger.debug('Subscription removed.')
	return redirect('all_blogs')