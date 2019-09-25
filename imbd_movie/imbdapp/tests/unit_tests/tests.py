import random
import math
import mock
from mock import call
import string

from django.test import TestCase
from django.conf import settings
from django.test import LiveServerTestCase

from imbdapp.models import Person, Genre, Movie
from imbdapp.tasks import *

class MockResponse:
	def __init__(self, json_data, status_code):
		self.text = json_data
		self.status_code = status_code
		self.url = ''

	def json(self):
		return json.loads(self.text)
	
def string_generator(size=10, chars=string.ascii_uppercase + string.digits):
	""" generates random string """
	return ''.join(random.choice(chars) for _ in range(size))

def decimal_generator():
	return float(('{0}.{1}').format(random.randint(0,999), random.randint(0,99)))

def make_person():
	person = Person()
	person.name = string_generator()
	person.facebook_likes = random.randint(0, 9999999)
	person.save()
	return person
	
def make_movie():
	movie = Movie()
	movie.movie_title = string_generator()
	movie.save()
	return movie

def make_genre():
	genre = Genre()
	genre.name = string_generator()
	genre.save()
	return genre

def make_movies_with_random_genres(genres):
	num_movies = random.randint(10, 999)
	movies = [make_movie() for i in range(num_movies)]
	for movie in movies:
		random_genre = random.choice(genres)
		movie.genres.add(random_genre)
	return movies
	
class PersonModelTest(TestCase):
	
	def setUp(self):
		self.person = make_person()
		
	def tearDown(self):
		pass
	
	def test_str(self):
		expected = self.person.name
		actual = self.person.__str__()
		self.assertEqual(expected, actual)
		
	def test_is_actor(self):
		self.movie = make_movie()
		
		expected = False
		actual = self.person.is_actor()
		self.assertEqual(expected, actual)
		
		self.movie.actors.add(self.person)
		expected = True
		actual = self.person.is_actor()
		self.assertEqual(expected, actual)
		
	def test_is_director(self):
		self.movie = make_movie()
		
		expected = False
		actual = self.person.is_director()
		self.assertEqual(expected, actual)
		
		self.movie.director = self.person
		self.movie.save()
		expected = True
		actual = self.person.is_director()
		self.assertEqual(expected, actual)
		
	@mock.patch('imbdapp.models.is_empty_value')
	def test_create(self, mock_is_empty_value):
		pass
		
class TasksTest(TestCase):
	
	def setUp(self):
		self.person = make_person()
		self.movie = make_movie()
		
	def tearDown(self):
		pass
	
	@mock.patch('imbdapp.models.is_empty_value')
	@mock.patch('imbdapp.models.Person.objects.get_or_create')
	def test_create_or_get_actors_from_row(self, mock_get_or_create, mock_is_empty_value):
		#test no empty values
		row = {
			'actor_1_name': string_generator(),
			'actor_2_name': string_generator(),
			'actor_3_name': string_generator(),
			'actor_1_facebook_likes': random.randint(0, 999),
			'actor_2_facebook_likes': random.randint(0, 999),
			'actor_3_facebook_likes': random.randint(0, 999),
		}
		expected = [make_person(), make_person(), make_person()]
		mock_get_or_create.side_effect = [(expected[0], True), (expected[1], True), (expected[2], True)] 
		mock_is_empty_value.side_effect = [False, False, False]
		create_mock_calls = []
		data = {'actor_1_name': row['actor_1_name'], 'facebook_likes': row['actor_1_facebook_likes']}
		create_mock_calls.append(call(**data))
		data = {'actor_2_name': row['actor_2_name'], 'facebook_likes': row['actor_2_facebook_likes']}
		create_mock_calls.append(call(**data))
		data = {'actor_3_name': row['actor_3_name'], 'facebook_likes': row['actor_3_facebook_likes']}
		create_mock_calls.append(call(**data))
		empty_mock_calls = [call(row['actor_1_facebook_likes']), call(row['actor_2_facebook_likes']), call(row['actor_3_facebook_likes'])]
		actual = create_or_get_actors_from_row(row)
		self.assertEqual(expected, actual)
		mock_get_or_create.has_calls(create_mock_calls)
		mock_is_empty_value.has_calls(empty_mock_calls)
		self.assertEqual(3, mock_get_or_create.call_count)
		mock_get_or_create.reset_mock()
		mock_is_empty_value.reset_mock()
		
		#test empty values
		row = {
			'actor_1_name': string_generator(),
			'actor_2_name': string_generator(),
			'actor_3_name': string_generator(),
			'actor_1_facebook_likes': random.randint(0, 999),
			'actor_2_facebook_likes': random.randint(0, 999),
			'actor_3_facebook_likes': random.randint(0, 999),
		}
		expected = [make_person(), make_person(), make_person()]
		mock_get_or_create.side_effect = [(expected[0], True), (expected[1], True), (expected[2], True)] 
		mock_is_empty_value.return_value = True
		create_mock_calls = []
		data = {'actor_1_name': row['actor_1_name'], 'facebook_likes': 0}
		create_mock_calls.append(call(**data))
		data = {'actor_2_name': row['actor_2_name'], 'facebook_likes': 0}
		create_mock_calls.append(call(**data))
		data = {'actor_3_name': row['actor_3_name'], 'facebook_likes': 0}
		create_mock_calls.append(call(**data))
		empty_mock_calls = [call(row['actor_1_facebook_likes']), call(row['actor_2_facebook_likes']), call(row['actor_3_facebook_likes'])]
		actual = create_or_get_actors_from_row(row)
		self.assertEqual(expected, actual)
		mock_get_or_create.has_calls(create_mock_calls)
		mock_is_empty_value.has_calls(empty_mock_calls)
		self.assertEqual(3, mock_get_or_create.call_count)
		
	@mock.patch('imbdapp.tasks.get_top_profitable_actors_by_total')
	@mock.patch('imbdapp.tasks.get_top_profitable_directors_by_total')
	@mock.patch('builtins.sorted')
	def test_get_top_profitable_persons_by_total(self, mock_sorted, mock_directors_by_total, mock_actors_by_total):
		random_actors = [make_person() for i in range(10)]
		random_directors = [make_person() for i in range(10)]
		combined_list = random_actors + random_directors
		for person in combined_list:
			person.profitability = random.randint(0, 999)
		mock_sorted.return_value = combined_list
		mock_actors_by_total.return_value = random_actors
		mock_directors_by_total.return_value = random_directors
		actual = get_top_profitable_persons_by_total()
		expected = combined_list[:10]
		self.assertEqual(expected, actual)
		mock_directors_by_total.assert_called_once_with()
		mock_actors_by_total.assert_called_once_with()
		self.assertEqual(1, mock_sorted.call_count)
		
		
		
