import datetime
import http.client
import json
import logging
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseServerError
from requests.adapters import HTTPAdapter

from common import common
from player.models import Game, Stats

headers = {
    "X-RapidAPI-Key": settings.X_RAPIDAPI_KEY,
    "X-RapidAPI-Host": settings.X_RAPIDAPI_HOST,
}

logger = logging.getLogger(__name__)


def insert_all_game_and_stats():
    all_game = get_all_past_game_data()
    with transaction.atomic():  # トランザクション開始
        for game_data in all_game:
            db_insert_game(game_data)

    insert_all_stats()


@transaction.atomic
def insert_game_and_stats():
    # DBに本日分のgameとstatsの情報を追加する関数
    # 昨日の日付取得
    today = datetime.datetime.now().date()  # 本日
    yesterday = today + datetime.timedelta(days=-1)  # 昨日
    # gameのデータをAPIから取得
    game_data = get_game_data(yesterday)
    if not game_data['response']:
        logger.error(f'NBA APIからゲームデータの取得に失敗しました。game_data:{game_data}')
    # APIから取得したデータをDBに格納
    game_id_list = db_insert_game(game_data)

    # statsのデータをAPIから取得
    for game_id in game_id_list:
        stats_data = get_stats_data(game_id)
        # APIから取得したデータをDBに格納
        db_insert_stats(stats_data)
    
    # 完了ログ出力
    logger.info(f'{yesterday}のgameとstatsデータを登録しました。')

def insert_all_stats():
    all_game_id = Game.objects.values_list('game_id', flat=True)
    print('get_stats_data呼び出し')
    for game_id in all_game_id:
        print('======================')
        stats_data = get_stats_data(game_id)
        db_insert_stats(stats_data)
    print('全てのstatsをDBに追加することができました。')

def start():
    # insert_all_game_and_stats()  # 初回時のみ実行
    scheduler = BackgroundScheduler()
    scheduler.add_job(insert_game_and_stats, 'cron', hour=12)  # 毎日12時に実行(UTC時間)(日本時間3時)
    scheduler.start()


def get_all_past_game_data():
    # 過去のゲームのデータをすべて取得する関数
    # すべてのシーズン取得
    url = f'https://api-nba-v1.p.rapidapi.com/seasons'
    all_seasons = call_api(url)

    all_game_data = []
    for season in all_seasons['response']:
        url = f'https://api-nba-v1.p.rapidapi.com/games?season={season}'
        game_data = call_api(url)
        all_game_data.append(game_data)

    return all_game_data


def get_game_data(yesterday):
    # APIから昨日のゲームデータを取得する関数
    try:
        url = f'https://api-nba-v1.p.rapidapi.com/games?date={yesterday}'
        game_data = call_api(url)
    except Exception as e:
        logger.error(f'ゲームデータの取得に失敗しました: {e}')
        return HttpResponseServerError()

    return game_data


def get_stats_data(game_id):
    # APIからgame_idでstatsを取得する関数
    try:
        url = f'https://api-nba-v1.p.rapidapi.com/players/statistics?game={game_id}'
        stats_data = call_api(url)
    except Exception as e:
        logger.error(f'statsデータの取得に失敗しました: {e}')
        return HttpResponseServerError()

    return stats_data

def db_insert_game(game_data):
    games = []
    game_id_list = []
    for response in game_data['response']:
        game_id = response['id']
        str_date = response['date']['start']
        try:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            date = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        except Exception as e:
            print(e)
        season = response['season']
        visitors_team_id = response['teams']['visitors']['id']
        visitors_point = response['scores']['visitors']['points']
        home_team_id = response['teams']['home']['id']
        home_point = response['scores']['home']['points']
        if visitors_point is None or home_point is None:
            continue
        else:
            win_team_id = visitors_team_id if visitors_point > home_point else home_team_id
        game = Game(game_id=game_id, date=date, season=season, visitors_team_id=visitors_team_id,
                    visitors_point=visitors_point, home_team_id=home_team_id, home_point=home_point, win_team_id=win_team_id)
        games.append(game)
        game_id_list.append(game_id)

    try:
        Game.objects.bulk_create(games)  # DB挿入
    except Exception as e:
        print(e)

    return game_id_list


def db_insert_stats(stats_data):
    print('db_insert_stats呼び出し')
    stats = []
    for response in stats_data['response']:
        game = Game(game_id=response['game']['id'])
        player_id = response['player']['id']
        team_id = response['team']['id']
        points = response['points']
        pos = response['pos']
        min = response['min']
        fgm = response['fgm']
        fga = response['fga']
        fgp = response['fgp']
        ftm = response['ftm']
        fta = response['fta']
        ftp = response['ftp']
        tpm = response['tpm']
        tpa = response['tpa']
        tpp = response['tpp']
        reb = response['totReb']
        assists = response['assists']
        pFouls = response['pFouls']
        steals = response['steals']
        turnovers = response['turnovers']
        blocks = response['blocks']
        if points is None or player_id is None:
            continue
        stats_obj = Stats(game=game, player_id=player_id, team_id=team_id, points=points,
                        pos=pos, min=min, fgm=fgm, fga=fga, fgp=fgp, ftm=ftm, fta=fta, ftp=ftp, tpm=tpm, tpa=tpa, tpp=tpp, reb=reb, assists=assists, pFouls=pFouls, steals=steals, turnovers=turnovers, blocks=blocks)
        stats.append(stats_obj)

    try:
        Stats.objects.bulk_create(stats)  # DB挿入
        print('DB挿入完了')
    except Exception as e:
        logger.error(f'statsのDB挿入でエラーが発生しました。')


class TooManyRequestsError(Exception):
    pass

# API呼び出し
def call_api(url):

    session = requests.Session()
    retries = requests.adapters.Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # API呼び出し
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response_data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        raise Exception(f'Error: {url} - {e}')

    return response_data