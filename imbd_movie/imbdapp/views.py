from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from imbdapp.models import Movie
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

def movies(request):
	"""shows all the movies in a table with pagination"""
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
	if 'filter_type' in request.GET:
		filter_type = request.GET['filter_type']
	else:
		filter_type = ''
	try:
		num_items = int(request.GET['num_items'])
	except:
		num_items = 10
	title, profitable_items = get_profitable_items(filter_type, num_items)
	context = {'items': profitable_items, 'title': title}
	return render(request, 'profitability.html', context)