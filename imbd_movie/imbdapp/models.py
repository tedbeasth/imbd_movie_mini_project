import uuid
import datetime
from datetime import timedelta
import os
import random

from django.db import models
from django.conf import settings
from django.utils import timezone

import pandas as pd

def is_empty_value(value):
	"""Checks if value is empty, None, or a pandas Null
		returns boolean
	"""
	if not value or value in [None, "nan", ''] or pd.isnull(value):
		return True
	return False

class ModelBase(models.Model):
	uu_id =  models.UUIDField(default=uuid.uuid4, editable=False)
	is_active = models.BooleanField(default = True)
	date_created = models.DateTimeField(auto_now_add = True)

	class Meta:
		abstract = True

class Person(ModelBase):
	name = models.CharField(max_length=30)
	facebook_likes = models.IntegerField(default=0)
	
	def __str__(self):
		return self.name
	
	@classmethod
	def create(cls, **kwargs):
		fb_likes = kwargs.get('facebook_likes', 0)
		if is_empty_value(fb_likes):
			fb_likes = 0
		person = cls(
			name = kwargs['name'],
			facebook_likes = fb_likes,
		)
		person.save()
		return person
	
	def is_actor(self):
		"""Checks if Person is in at least one movie as an actor
			returns boolean
		"""
		if self.movies_as_actor.all():
			return True
		return False
	
	def is_director(self):
		"""Checks if Person is in at least one movie as a director
			returns boolean
		"""
		if self.movies_as_director.all():
			return True
		return False
	
class Genre(ModelBase):
	name = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name
	
class Movie(ModelBase):
	duration = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	gross = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
	imdb_score = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)
	aspect_ratio = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
	budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
	
	num_voted_users = models.IntegerField(default=0)
	num_user_for_reviews = models.IntegerField(default=0)
	facenumber_in_poster = models.IntegerField(default=0)
	cast_total_facebook_likes = models.IntegerField(default=0)
	movie_facebook_likes = models.IntegerField(default=0)
	num_critic_for_reviews = models.IntegerField(default=0)
	
	color = models.CharField(max_length=30, blank=True, null=True)
	movie_title = models.CharField(max_length=30, blank=True, null=True)
	plot_keywords = models.CharField(max_length=100, blank=True, null=True)
	language = models.CharField(max_length=30, blank=True, null=True)
	country = models.CharField(max_length=30, blank=True, null=True)
	content_rating = models.CharField(max_length=30, blank=True, null=True) #could make this a choice field
	title_year = models.CharField(max_length=30, blank=True, null=True) #could be a datetime field
	movie_imdb_link = models.URLField(max_length=100, blank=True, null=True)
	
	actors = models.ManyToManyField(Person, related_name="movies_as_actor")
	director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='movies_as_director', blank=True, null=True)
	genres = models.ManyToManyField(Genre, related_name='movies_set')
	
	def __str__(self):
		return self.movie_title
	
	@classmethod
	def create(cls, actors=[], genres=[], **kwargs):
		#TODO add security and error handling to check to make sure all fields in kwargs are attributes in the movie model as well as null values
		movie = cls()
		for field in kwargs:
			if is_empty_value(kwargs[field]):
				continue
			setattr(movie, field, kwargs[field])
		movie.save()
		if actors:
			movie.actors.add(*actors)
		if genres:
			movie.genres.add(*genres)
		return movie
	
	@property
	def get_genres(self):
		return self.get_genres_names()
	
	def get_actors_names(self):
		""" returns string of all actors names for movie separated by commas"""
		return ", ".join([actor.name for actor in self.actors.all()])
	
	def get_genres_names(self):
		""" returns string of all genres names for movie separated by commas"""
		return ", ".join([genre.name for genre in self.genres.all()])