from django.contrib import admin
from .models import Game

class GameAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("name", "app_id", "release_date", "price", "score_rank")

    # Filters in the sidebar
    list_filter = ('release_date', 'price', 'score_rank')

    # Add search functionality
    search_fields = ('name', 'app_id', 'about_the_game', 'developers', 'publishers', 'genres', 'tags')

    # Specify the fields to be searched
    # Ensure 'search_fields' contains fields you want to search by
    # Removed duplicate 'search_fields' entry
    
    # Add ordering to list view
    ordering = ('-release_date',)


    # Make fields editable in the list view
    list_editable = ('price',)

admin.site.register(Game, GameAdmin)
