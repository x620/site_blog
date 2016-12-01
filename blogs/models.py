# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse

from site_blog.settings import DOMAIN, DEFAULT_FROM_EMAIL


class Blog(models.Model):
	name = models.CharField('Name of blog', max_length=100, blank=True, null=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return 'Blog: %s' % self.user


class Entry(models.Model):
	blog = models.ForeignKey(Blog)
	title = models.CharField('Title', max_length=255, blank=True, null=True)
	body = models.TextField('Entry')
	pub_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Entries'

	def __unicode__(self):
		return '%s (author: %s)' % (self.title, self.blog.user)


class Subscription(models.Model):
	user = models.ForeignKey(User)
	blog = models.ForeignKey(Blog)

	def __unicode__(self):
		return 'Subscription: %s' % self.blog.user


class ReadEntry(models.Model):
	user = models.ForeignKey(User)
	entry = models.ForeignKey(Entry)

	def __unicode__(self):
		return '%s' % self.entry


@receiver(post_save, sender=User)
def create_user_blog(sender, instance, created, **kwargs):
	if created and not instance.is_staff:
		blog = Blog(user=instance)
		blog.save()


@receiver(post_save, sender=Entry)
def create_entry(sender, instance, created, **kwargs):
	if created:
		notification_for_subscriber(instance.blog)


def notification_for_subscriber(blog):
	"""
	Sending email notification for subscribers
	"""
	subscribers = Subscription.objects.filter(blog=blog)
	if subscribers.exists():
		recipients = [sub.user.email for sub in subscribers if sub.user.email]
		if recipients:
			sbj = 'New post in the your subscriptions'
			message = '''
Hi.
You subscribed on the blog %s.
This blog publish new post.
Go to the blog that see it: http://%s%s
''' % (blog, DOMAIN, reverse('account'))
			# logger.debug('Send notifications. Recipients: %s' % recipients)
			send_mail(sbj, message, DEFAULT_FROM_EMAIL, recipients)
