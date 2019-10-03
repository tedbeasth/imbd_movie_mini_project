from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from imbdapp.models import Movie, Genre, Person
from imbdapp.tasks import *

def paginator_helper(query_set, page, num_per_page=50):
	"""creates paginator"""
	paginator = Paginator(query_set, num_per_page)
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)
	return data

def actors_and_directors(request):
	"""shows all the Persons in a table with pagination"""
	people = Person.objects.filter(is_active=True)
	page = request.GET.get('page', 1)
	people_data = paginator_helper(people, page, 50)
	context = {'people': people_data}
	return render(request, 'people.html', context)

def genres(request):
	"""shows all the Genres in a table with pagination"""
	genres = Genre.objects.filter(is_active=True)
	page = request.GET.get('page', 1)
	genres_data = paginator_helper(genres, page, 50)
	context = {'genres': genres_data}
	return render(request, 'genres.html', context)

def movies(request):
	"""shows all the Movies in a table with pagination"""
	movies = Movie.objects.filter(is_active=True)
	page = request.GET.get('page', 1)
	movies_data = paginator_helper(movies, page, 50)
	context = {'movies': movies_data}
	return render(request, 'movies.html', context)

def get_profitable_items(filter_type, num_items=10):
	"""helper function to determine which calculation to perform. returns title and items"""
	if filter_type == 'genre_total':
		title = "Genres By Total"
		profitable_items = get_top_profitable_genres_by_total(num_items)
	elif filter_type == 'genre_average':
		title = "Genres By Average"
		profitable_items = get_top_profitable_genres_by_average(num_items)
	elif filter_type == 'actors':
		title = "Actors By Total"
		profitable_items = get_top_profitable_actors_by_total(num_items)
	elif filter_type == 'directors':
		title = "Directors By Total"
		profitable_items = get_top_profitable_directors_by_total(num_items)
	elif filter_type == 'people':
		title = "People By Total"
		profitable_items = get_top_profitable_persons_by_total(num_items)
	else:
		title = "Please select one of the filter options above"
		profitable_items = []
	return title, profitable_items
	
def profitability(request):
	"""calculates most profitable items depending on the filter_type and shows them in a table"""
	filter_type = request.GET.get('filter_type', '')
	try:
		num_items = int(request.GET['num_items'])
	except:
		num_items = 10
	title, profitable_items = get_profitable_items(filter_type, num_items)
	context = {'items': profitable_items, 'title': title}
	return render(request, 'profitability.html', context)