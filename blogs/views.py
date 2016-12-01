# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from forms import LoginForm, AddEntryForm
from .models import Blog, Entry, Subscription, ReadEntry, notification_for_subscriber

import logging
logger = logging.getLogger(__name__)


def get_subscriptions(user):
	"""
	Return subscriptions
	"""
	return Subscription.objects.filter(user=user)


def all_subscription_blogs(user):
	"""
	Return all blogs which user subscription
	"""
	return [sub.blog for sub in get_subscriptions(user)]


def all_no_subscription_blogs(user):
	"""
	Return all blogs which user no subscription
	"""
	all_blogs = Blog.objects.exclude(user=user)
	return [blog for blog in all_blogs if blog not in all_subscription_blogs(user)]


def get_entries_from_subscription_blogs(user):
	"""
	Return queryset entries in the subscription blogs
	"""
	subs = get_subscriptions(user)
	entry_ids = []
	for sub in subs:
		entry_ids += list(sub.blog.entry_set.all().values_list('id', flat=True))
	return Entry.objects.filter(pk__in=entry_ids).order_by('-pub_date')


def get_unread_entries_from_subscription_blogs(user):
	"""
	Return queryset entries in the subscription blogs without read entries
	"""
	entries = get_entries_from_subscription_blogs(user)
	read_entries = ReadEntry.objects.filter(user=user)
	read_entries_ids = [read_entry.entry_id for read_entry in read_entries]
	return entries.exclude(pk__in=read_entries_ids)


class MainView(FormView):
	template_name = 'main.html'
	form_class = LoginForm
	success_url = reverse_lazy('account')

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('account')
		return super(MainView, self).get(request, *args, **kwargs)

	def form_valid(self, form):
		if self.request.method == 'POST':
			send_form = LoginForm(self.request.POST)
			if send_form.is_valid():
				username = send_form.cleaned_data['username']
				password = send_form.cleaned_data['password']

				user = authenticate(username=username, password=password)
				if user is not None:
					login(self.request, user)
					return super(MainView, self).form_valid(form)
			return redirect('login_error')

	def get_context_data(self, **kwargs):
		context = super(MainView, self).get_context_data(**kwargs)
		context['login_form'] = self.form_class
		context['main'] = True
		return context


class AccountView(LoginRequiredMixin, TemplateView):
	login_url = reverse_lazy('index')
	template_name = 'account.html'

	def get_context_data(self, **kwargs):
		context = super(AccountView, self).get_context_data(**kwargs)
		context['main'] = True
		context['sub_blogs'] = get_subscriptions(self.request.user)
		context['sub_entries'] = get_unread_entries_from_subscription_blogs(self.request.user)
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
				# Save entry in DB
				blog = Blog.objects.get(user=self.request.user)
				entry = Entry(blog=blog, body=body)
				entry.title = title
				entry.save()
				# Send email notification to subscribers
				notification_for_subscriber(blog)
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
		context = super(AllBlogsView, self).get_context_data(**kwargs)
		context['subs_blog_list'] = all_no_subscription_blogs(self.request.user)
		context['unsubs_blog_list'] = all_subscription_blogs(self.request.user)
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


class ErrorView(TemplateView):
	pass


def logout_view(request):
	logout(request)
	return redirect('index')


def subscription(request, pk):
	blog = get_object_or_404(Blog, pk=int(pk))
	new_subscription = Subscription(user=request.user, blog=blog)
	new_subscription.save()
	return redirect('all_blogs')


def unsubscription(request, pk):
	blog = get_object_or_404(Blog, pk=int(pk))
	subscriptions = Subscription.objects.filter(user=request.user, blog=blog)

	# Remove info about read entries in the unsubscribe blog
	for sub in subscriptions:
		ReadEntry.objects.filter(user=request.user, entry__blog=sub.blog).delete()

	subscriptions.delete()
	return redirect('all_blogs')


def read(request, pk):
	entry = get_object_or_404(Entry, pk=int(pk))
	read_entry = ReadEntry(user=request.user, entry=entry)
	read_entry.save()
	logger.debug('Entry %s (%s) was read user: %s' % (entry.id, entry.title, request.user))
	return redirect('account')
