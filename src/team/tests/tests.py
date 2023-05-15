import os
import json
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from team.views import extract_nba_franchise_and_not_all_ster
from team.tests.test_data import response_team_list
from team.tests.test_data import response_player_list
from team.tests.test_data import nba_franchise_and_not_all_ster_data

# Create your tests here.


class TeamViewTests(TestCase):
    def setUp(self):
        self.client = Client()
    
    @patch('team.views.call_api')
    def test_team_list_ok(self, mock_call_api):
        """
        team_list関数正常系
        """
        with open(os.path.join(settings.BASE_DIR, 'team/tests/test_data/east_team.json'), 'r') as f:
            east_data = json.load(f)
        with open(os.path.join(settings.BASE_DIR, 'team/tests/test_data/west_team.json'), 'r') as f:
            west_data = json.load(f)
        mock_call_api.side_effect = [
            east_data,  # 1回目の呼び出し
            west_data,  # 2回目の呼び出し
        ]

        response = self.client.get(reverse('team:teams'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['teams'], response_team_list.context)

    @patch('team.views.call_api')
    def test_player_list_by_team_id_ok(self, mock_call_api):
        """
        player_list_by_team_id関数正常系
        team_id2のプレーヤの情報が正しく取得できるかの確認
        """

        with open(os.path.join(settings.BASE_DIR, 'team/tests/test_data/team_id2.json'), 'r') as f:
            team_id2 = json.load(f)
        with open(os.path.join(settings.BASE_DIR, 'team/tests/test_data/seasons.json'), 'r') as f:
            seasons = json.load(f)
        with open(os.path.join(settings.BASE_DIR, 'team/tests/test_data/players_by_team_id2.json'), 'r') as f:
            player_list = json.load(f)
        mock_call_api.side_effect = [
            team_id2,   # 1回目の呼び出し
            seasons,    # 2回目の呼び出し
            player_list  # 3回目の呼び出し
        ]

        response = self.client.get(reverse('team:player_list', args=(2,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['current_team'], response_player_list.current_team)
        self.assertEqual(
            response.context['player_list'], response_player_list.player_list)
        
    def test_extract_nba_franchise_func_ok(self):
        """
        extract_nba_franchise関数正常系
        nba_franchise所属のEastチームが正しく取得できるかの確認
        """
        with open(os.path.join(settings.BASE_DIR, 'team/tests/test_data/east_team.json'), 'r') as f:
            east_data = json.load(f)
        
        response_data = nba_franchise_and_not_all_ster_data.east_team
        
        self.assertEqual(extract_nba_franchise_and_not_all_ster(east_data), response_data)
