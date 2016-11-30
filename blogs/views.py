# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from forms import LoginForm

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
		return context


class LoginErrorView(TemplateView):
	template_name = 'error_login.html'


def logout_view(request):
	logout(request)
	return redirect('index')


# Account
class AccountView(LoginRequiredMixin, TemplateView):
	login_url = reverse_lazy('index')
	template_name = 'account.html'
