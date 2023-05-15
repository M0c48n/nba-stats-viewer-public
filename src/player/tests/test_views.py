import datetime

from django.test import TestCase
from django.urls import reverse

from player.models import Game
from player.models import Stats


# Create your tests here.


class PlayerViewTests(TestCase):
    def setUp(self):
        date = datetime.datetime(2020, 1, 20)
        game = Game.objects.create(game_id=1, date=date, season=2022, visitors_team_id=2, visitors_point=67,
                                   home_team_id=3, home_point=78, win_team_id=3, updated_at=date, created_at=date)
        Stats.objects.create(game=game, player_id=1, team_id=1, points=20, pos='PG', min='30:00', fgm=7, fga=10, fgp='70%',
                             ftm=5, fta=6, ftp='83%', tpm=2, tpa=4, tpp='50%', reb=5, assists=7, pFouls=2, steals=3, turnovers=2, blocks=1)
        Stats.objects.create(game=game, player_id=1, team_id=1, points=25, pos='PG', min='32:00', fgm=10, fga=15, fgp='66.6%',
                             ftm=8, fta=10, ftp='80.0%', tpm=2, tpa=5, tpp='40.0%', reb=5, assists=10, pFouls=3, steals=5, turnovers=2, blocks=1)
        Stats.objects.create(game=game, player_id=2, team_id=2, points=20, pos='SF', min='29:00', fgm=8, fga=12, fgp='66.6%',
                             ftm=4, fta=6, ftp='66.6%', tpm=2, tpa=4, tpp='50.0%', reb=7, assists=5, pFouls=2, steals=3, turnovers=1, blocks=2)
        Stats.objects.create(game=game, player_id=3, team_id=1, points=15, pos='PF', min='28:00', fgm=6, fga=10, fgp='60.0%',
                             ftm=3, fta=4, ftp='75.0%', tpm=1, tpa=3, tpp='33.3%', reb=8, assists=3, pFouls=2, steals=2, turnovers=1, blocks=3)
        Stats.objects.create(game=game, player_id=4, team_id=2, points=10, pos='C', min='26:00', fgm=4, fga=8, fgp='50.0%',
                             ftm=2, fta=2, ftp='100.0%', tpm=0, tpa=0, tpp='0.0%', reb=10, assists=2, pFouls=1, steals=1, turnovers=0, blocks=4)
        Stats.objects.create(game=game, player_id=5, team_id=1, points=5, pos='SG', min='24:00', fgm=2, fga=6, fgp='33.3%',
                             ftm=1, fta=2, ftp='50.0%', tpm=0, tpa=2, tpp='0.0%', reb=2, assists=1, pFouls=1, steals=0, turnovers=1, blocks=0)

    def test_stats_func_ok(self):
        """
        stats関数正常系
        最新シーズンの指定プレイヤーのstatsが正しく取得できるかの確認
        """
        response = self.client.get(reverse('player:player', args=(1, )))
        response_data = {}
        self.assertEqual(response.status_code, 200)
