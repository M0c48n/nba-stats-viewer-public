from django.urls import path
from . import views

app_name = 'player'
urlpatterns = [
    path('player/<int:player_id>', views.stats, name='player'),
    
]
