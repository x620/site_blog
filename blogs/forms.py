# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(
		label='',
		max_length=50,
		widget=forms.TextInput(attrs={'placeholder': 'Login', 'class': 'form-control'})
	)
	password = forms.CharField(
		label='',
		max_length=50,
		widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
	)
