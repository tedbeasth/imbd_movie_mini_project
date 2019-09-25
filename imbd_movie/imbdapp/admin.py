from django.contrib import admin
from django.urls import reverse
from imbdapp.models import Genre, Person, Movie

class GenreAdmin(admin.ModelAdmin):
    search_fields = ('pk',)
    list_display = ['pk', 'is_active', 'name']
    
admin.site.register(Genre, GenreAdmin)

class PersonAdmin(admin.ModelAdmin):
    search_fields = ('pk',)
    list_display = ['pk', 'is_active', 'name', 'facebook_likes']
    
admin.site.register(Person, PersonAdmin)

class MovieAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['pk', 'is_active', 'movie_title', 'gross', 'budget', 'get_genres_names', 'director', 'get_actors_names']
    
admin.site.register(Movie, MovieAdmin)
