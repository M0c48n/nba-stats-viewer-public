from django.urls import path
from . import views

app_name = 'team'
urlpatterns = [
    path('', views.team_list, name='top'),
    path('teams/', views.team_list, name='teams'),
    path('team/<int:team_id>', views.player_list_by_team_id, name='player_list')
]
