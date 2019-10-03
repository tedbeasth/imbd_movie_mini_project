from django.urls import path
from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [

    path('movies/', views.movies, name='movies'),
    path('people/', views.actors_and_directors, name='actors_and_directors'),
    path('genres/', views.genres, name='genres'),
    url(r'^profitability/$', views.profitability, name='profitability'),
    url(r'^$', RedirectView.as_view(url='/movies')),

]