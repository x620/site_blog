# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Blog, Entry


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('user', 'name', 'id')
	search_fields = ('name',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
	list_display = ('title', 'body', 'blog', 'pub_date', 'id')
	search_fields = ('title', 'body')
