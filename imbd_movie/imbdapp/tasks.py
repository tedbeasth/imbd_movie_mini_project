import csv
import pandas as pd

from django.db import transaction
from django.db.models import Sum, Avg

from imbdapp.models import *

@transaction.atomic
def import_movies_csv():
	""" imports from a csv file using pandas and populates the database. Csv file must be in the correct format
	"""
	#TODO account for duplicate movie titles?
	#using pandas
	df = pd.read_csv('imbdapp/csv_files/movie_metadata.csv', iterator=True, chunksize=1000)
	for chunk in df:
		for index, row in chunk.iterrows():
			actors = create_or_get_actors_from_row(row)
			genres = create_or_get_genres_from_row(row)
			director = create_or_get_director_from_row(row)
			row["director"] = director
			Movie.create(actors=actors, genres=genres, **row)
			
	"""
	#using python's DictReader
	with open('imbdapp/csv_files/movie_metadata.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			actors = create_or_get_actors_from_row(row)
			director = create_or_get_director_from_row(row)
			row["director"] = director
			Movie.create(actors=actors, **row)
			
				MyModel.objects.bulk_create([
			MyModel(**data) for data in model_data
			])
	"""

def create_or_get_actors_from_row(row):
	actors = []
	for actor_count in range(1,4):
		actor_name = row["actor_{}_name".format(actor_count)]
		facebook_likes = row["actor_{}_facebook_likes".format(actor_count)]
		if is_empty_value(facebook_likes):
			facebook_likes = 0
		actor_data = {'name': actor_name, 'facebook_likes': facebook_likes}
		actor, created = Person.objects.get_or_create(**actor_data)
		actors.append(actor)
	return actors

def create_or_get_genres_from_row(row):
	genres = []
	genre_names = row.pop('genres').split('|')
	for genre_name in genre_names:
		genre_data = {'name': genre_name}
		genre, created = Genre.objects.get_or_create(**genre_data)
		genres.append(genre)
	return genres

def create_or_get_director_from_row(row):
	facebook_likes = row["director_facebook_likes"]
	if is_empty_value(facebook_likes):
		facebook_likes = 0
	director_data = {'name': row["director_name"], 'facebook_likes': facebook_likes}
	director, created = Person.objects.get_or_create(**director_data)
	return director

def get_top_profitable_genres_by_total(num_genres=10):
	""" Returns the top genres based on profitability.
		profitability is calculated by total gross - total budget
		descreasing order
	"""
	top_genres = Genre.objects.annotate(profitability=Sum('movies_set__gross') - Sum('movies_set__budget')).order_by('-profitability')[:num_genres]
	return top_genres

def get_top_profitable_genres_by_average(num_genres=10):
	""" Returns the top genres based on profitability.
		profitability is calculated by average gross - average budget
		descreasing order
	"""
	top_genres = Genre.objects.annotate(profitability=Avg('movies_set__gross') - Avg('movies_set__budget')).order_by('-profitability')[:num_genres]
	return top_genres

def get_top_profitable_actors_by_total(num_genres=10):
	""" Returns the top actors based on profitability.
		profitability is calculated by total gross - total budget
		descreasing order
	"""
	top_actors = Person.objects.annotate(profitability=Avg('movies_as_actor__gross') - Avg('movies_as_actor__budget')).order_by('-profitability')[:num_genres]
	return top_actors

def get_top_profitable_directors_by_total(num_genres=10):
	""" Returns the top directors based on profitability.
		profitability is calculated by total gross - total budget
		descreasing order
	"""
	top_directors = Person.objects.annotate(profitability=Avg('movies_as_director__gross') - Avg('movies_as_director__budget')).order_by('-profitability')[:num_genres]
	return top_directors

def get_top_profitable_persons_by_total(num_genres=10):
	""" Returns the top persons based on profitability.
		profitability is calculated by total gross - total budget
		persons can either be the director or the actor
		descreasing order
	"""
	top_directors = get_top_profitable_directors_by_total()
	top_actors = get_top_profitable_actors_by_total()
	top_persons_list = list(top_actors) + list(top_directors)
	sorted_persons = sorted(top_persons_list, key=lambda person: person.profitability, reverse=True)[:10]
	return sorted_persons