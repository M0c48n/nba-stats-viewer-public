import logging

import requests
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseServerError
from django.shortcuts import render
from requests.adapters import HTTPAdapter

from player.models import Stats

# Create your views here.
logger = logging.getLogger(__name__)

# RapidAPIを呼び出すためのヘッダ情報を設定
headers = {
    "X-RapidAPI-Key": settings.X_RAPIDAPI_KEY,
    "X-RapidAPI-Host": settings.X_RAPIDAPI_HOST,
}


def stats(request, player_id):
    """
    選択したプレイヤーのスタッツ情報を表示するビュー関数
    """
    # RapidAPIから選択したプレイヤーの名前を取得
    try:
        url = f'https://api-nba-v1.p.rapidapi.com/players?id={player_id}'
        current_player = call_api(url)
    except Exception as e:
        logger.error(f'選手情報の取得に失敗しました: {e}')
        return HttpResponseServerError()
    # プレイヤーの名前を取得
    plyer_name = f"{current_player['response'][0]['firstname']} {current_player['response'][0]['lastname']}"

    # RapidAPIからシーズン情報を取得
    try:
        url = f'https://api-nba-v1.p.rapidapi.com/seasons'
        seasons = call_api(url)
    except Exception as e:
        logger.error(f'シーズン情報の取得に失敗しました: {e}')
        return HttpResponseServerError()
    # すべてのシーズンを取得
    all_seasons = seasons['response']
    # 降順にソート
    all_seasons.sort(reverse=True)
    # 選択されたシーズンを取得
    selected_season = request.GET.get('season')
    if selected_season is None:
        # クエリパラメータに'season'が指定されていない場合は最新シーズンを設定
        selected_season = all_seasons[0]

    # DBから選択したプレイヤー、選択したシーズンのstatsを日付の降順に取得
    db_stats = Stats.objects.select_related('game').filter(
        player_id=player_id, game__season=selected_season
    ).order_by('-game__date')
    # 取得したstatsから表示用のリストを作成
    stats_list = create_stats_list(db_stats)

    # ページネーターを作成（1ページあたりデータ数20）
    paginator = Paginator(stats_list, 20)
    # クエリパラメータから現在のページ番号を取得
    page = request.GET.get('page')

    try:
        # 指定されたページ番号のデータを取得
        stats_list = paginator.page(page)
    except PageNotAnInteger:
        # ページ番号が整数でない場合は、最初のページを表示
        stats_list = paginator.page(1)
    except EmptyPage:
        # 指定したページ番号が存在しない場合は、最後のページを表示
        stats_list = paginator.page(paginator.num_pages)

    context = {
        'current_player_name': plyer_name,
        'stats_list': stats_list,
        'all_seasons': all_seasons,
        'selected_season': selected_season
    }

    return render(request, 'player/stats.html', context)


def call_api(url):
    """
    指定されたURLにGETリクエストを送信し、レスポンスをJSON形式で返す
    """
    # リトライを設定したセッションを作成
    session = requests.Session()
    retries = requests.adapters.Retry(
        total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        # API呼び出し
        response = session.get(url, headers=headers, timeout=10)
        # レスポンスがエラーだった場合に例外を発生させる
        response.raise_for_status()
        # レスポンスボディをJSONとして解析
        response_data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        # リクエストやレスポンスの処理中にエラーが発生した場合は例外を発生させる
        raise Exception(f'Error: {url} - {e}')

    return response_data


def create_stats_list(db_stats):
    """
    statsオブジェクトのリストから表示用のstatsリストを作成
    """
    return [
        {
            'date': s.game.date,
            'win_frag': s.team_id == s.game.win_team_id,
            'game_point': f'{s.game.visitors_point}-{s.game.home_point}',
            'min': s.min,
            'fg': f'{s.fgm}-{s.fga}',
            'fg_pct': s.fgp,
            'three_pt': f'{s.tpm}-{s.tpa}',
            'three_pt_pct': s.tpp,
            'ft': f'{s.ftm}-{s.fta}',
            'ft_pct': s.ftp,
            'reb': s.reb,
            'ast': s.assists,
            'blk': s.blocks,
            'stl': s.steals,
            'pf': s.pFouls,
            'to': s.turnovers,
            'pts': s.points
        } for s in db_stats
    ]
