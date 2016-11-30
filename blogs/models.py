# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_blog(sender, instance, created, **kwargs):
	if created and not instance.is_staff:
		blog = Blog(user=instance)
		blog.save()


class Blog(models.Model):
	name = models.CharField('Name of blog', max_length=100, blank=True, null=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return 'Blog: %s' % self.user


class Entry(models.Model):
	blog = models.ForeignKey(Blog)
	title = models.CharField('Title', max_length=255, blank=True, null=True)
	body = models.TextField('Entry')
	pub_date = models.DateField()

	def __unicode__(self):
		return '%s (author: %s)' % (self.title, self.blog.user)
