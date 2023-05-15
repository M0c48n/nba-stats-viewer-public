import datetime
import logging

import requests
from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import render
from requests.adapters import HTTPAdapter

from common import common

# Create your views here.
logger = logging.getLogger(__name__)

headers = {
    "X-RapidAPI-Key": settings.X_RAPIDAPI_KEY,
    "X-RapidAPI-Host": settings.X_RAPIDAPI_HOST
}


def team_list(request):
    # チームリストを返却する関数
    try:
        # 外部APIからEastチームの取得
        url = f'https://api-nba-v1.p.rapidapi.com/teams?conference=East'
        east_data = call_api(url)
        # 外部APIからWestチームの取得
        url = f'https://api-nba-v1.p.rapidapi.com/teams?conference=West'
        west_data = call_api(url)
    except Exception as e:
        logger.error(f'チーム情報の取得に失敗しました: {e}')
        return HttpResponseServerError()
    # nbaFranchiseかつallStarではないチームを抽出
    east_teams = extract_nba_franchise_and_not_all_ster(east_data)
    west_teams = extract_nba_franchise_and_not_all_ster(west_data)
    # 返却値設定
    context = {'teams': {'east_teams': east_teams, 'west_teams': west_teams}}

    return render(request, 'team/team_list.html', context)


def player_list_by_team_id(request, team_id):
    # チームIDからプレイヤーのリストを返却する関数
    try:
        # 選択したチームのチーム名とロゴを取得
        url = f'https://api-nba-v1.p.rapidapi.com/teams?id={team_id}'
        current_team = call_api(url)
        team_name = current_team['response'][0]['name']
        team_logo = current_team['response'][0]['logo']
        # 最新のシーズンを取得する
        url = f'https://api-nba-v1.p.rapidapi.com/seasons'
        seasons = call_api(url)
        latest_season = seasons['response'][-1]
        # チームのプレイヤーの取得
        url = f'https://api-nba-v1.p.rapidapi.com/players?team={team_id}&season={latest_season}'
        player_list = call_api(url)
    except Exception as e:
        logger.error(f'プレイヤー情報の取得に失敗しました: {e}')
        return HttpResponseServerError()
    # 返却データ用にフォーマット
    formatted_player_list = format_player_list(player_list)
    context = {'current_team': {'name': team_name, 'logo': team_logo},
               'player_list': formatted_player_list}

    return render(request, 'team/player_list.html', context)


def extract_nba_franchise_and_not_all_ster(data):
    # nbaFranchiseがtrueのチームのみ抽出
    delete_index = []
    for i, response in enumerate(data['response']):
        if not response['nbaFranchise'] or response['allStar']:
            delete_index.append(i)

    for index in sorted(delete_index, reverse=True):
        data['response'].pop(index)

    return data['response']


def format_player_list(player_list):
    # 返却データ用にフォーマットする処理
    result = []
    for response in (player_list['response']):
        id = response['id']
        name = f"{response['firstname']} {response['lastname']}"
        position = response['leagues']['standard']['pos']
        weight = response['weight']['kilograms']
        height = response['height']['meters']
        # 誕生日から現在の年齢を算出する
        if response['birth']['date']:
            birthday_str = response['birth']['date'].split('-')
            birthday = datetime.date(int(birthday_str[0]),
                                     int(birthday_str[1]), int(birthday_str[2]))
            today = datetime.date.today()
            age = (int(today.strftime("%Y%m%d")) -
                   int(birthday.strftime("%Y%m%d"))) // 10000
        else:
            age = None

        result.append({'id': id, 'name': name, 'position': position,
                      'weight': weight, 'height': height, 'age': age})

    return result


def call_api(url):

    session = requests.Session()
    retries = requests.adapters.Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # API呼び出し
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response_data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        raise Exception(f'Error: {url} - {e}')

    return response_data
