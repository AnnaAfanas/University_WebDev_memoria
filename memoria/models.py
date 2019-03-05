# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models


class Book(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	name = models.CharField(max_length=200) 
	comment = models.TextField(blank=True)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name


class Film(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	name = models.CharField(max_length=200) 
	comment = models.TextField(blank=True)
	published_date = models.DateTimeField(blank=True, null=True)


	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name


class TVSeries(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	name = models.CharField(max_length=200) 
	comment = models.TextField(blank=True)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name
