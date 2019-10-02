from django.urls import path
from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [

    path('movies/', views.movies, name='movies'),
    url(r'^profitability/$', views.profitability, name='profitability'),
    url(r'^$', RedirectView.as_view(url='/movies')),

]