import datetime

from django.test import TestCase

from ..models import Game
from player.ap_scheduler import db_insert_game

# Create your tests here.


class ApSchedulerTests(TestCase):
    def db_insert_game_func_ok(self):
        """
        get_game_data関数正常系
        ゲームデータが正しく取得できるかの確認
        """
        sample_game_data = {
            "get": "games/",
            "parameters": {
                "date": "2023-02-01"
            },
            "errors": [],
            "results": 5,
            "response": [
                {
                    "id": 1000,
                    "league": "standard",
                    "season": 2022,
                    "date": {
                        "start": "2023-02-01T00:00:00.000Z",
                        "end": None,
                        "duration": None
                    },
                    "stage": 2,
                    "status": {
                        "clock": None,
                        "halftime": False,
                        "short": 3,
                        "long": "Finished"
                    },
                    "periods": {
                        "current": 4,
                        "total": 4,
                        "endOfPeriod": False
                    },
                    "arena": {
                        "name": None,
                        "city": None,
                        "state": None,
                        "country": None
                    },
                    "teams": {
                        "visitors": {
                            "id": 20,
                            "name": "Miami Heat",
                            "nickname": "Heat",
                            "code": "MIA",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/1/1c/Miami_Heat_-_Logo.svg/1200px-Miami_Heat_-_Logo.svg.png"
                        },
                        "home": {
                            "id": 7,
                            "name": "Cleveland Cavaliers",
                            "nickname": "Cavaliers",
                            "code": "CLE",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/0/06/Cavs_de_Cleveland_logo_2017.png/150px-Cavs_de_Cleveland_logo_2017.png"
                        }
                    },
                    "scores": {
                        "visitors": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "24",
                                "31",
                                "24",
                                "21"
                            ],
                            "points": 100
                        },
                        "home": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "26",
                                "26",
                                "27",
                                "18"
                            ],
                            "points": 97
                        }
                    },
                    "officials": [],
                    "timesTied": None,
                    "leadChanges": None,
                    "nugget": None
                },
                {
                    "id": 1001,
                    "league": "standard",
                    "season": 2022,
                    "date": {
                        "start": "2023-02-01T00:30:00.000Z",
                        "end": None,
                        "duration": None
                    },
                    "stage": 2,
                    "status": {
                        "clock": None,
                        "halftime": False,
                        "short": 3,
                        "long": "Finished"
                    },
                    "periods": {
                        "current": 4,
                        "total": 4,
                        "endOfPeriod": False
                    },
                    "arena": {
                        "name": None,
                        "city": None,
                        "state": None,
                        "country": None
                    },
                    "teams": {
                        "visitors": {
                            "id": 17,
                            "name": "Los Angeles Lakers",
                            "nickname": "Lakers",
                            "code": "LAL",
                            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Los_Angeles_Lakers_logo.svg/220px-Los_Angeles_Lakers_logo.svg.png"
                        },
                        "home": {
                            "id": 24,
                            "name": "New York Knicks",
                            "nickname": "Knicks",
                            "code": "NYK",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/3/34/Knicks_de_NY.png"
                        }
                    },
                    "scores": {
                        "visitors": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "29",
                                "23",
                                "34",
                                "28",
                                "15"
                            ],
                            "points": 129
                        },
                        "home": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "24",
                                "29",
                                "30",
                                "31",
                                "9"
                            ],
                            "points": 123
                        }
                    },
                    "officials": [],
                    "timesTied": None,
                    "leadChanges": None,
                    "nugget": None
                },
                {
                    "id": 1003,
                    "league": "standard",
                    "season": 2022,
                    "date": {
                        "start": "2023-02-01T01:00:00.000Z",
                        "end": None,
                        "duration": None
                    },
                    "stage": 2,
                    "status": {
                        "clock": None,
                        "halftime": False,
                        "short": 3,
                        "long": "Finished"
                    },
                    "periods": {
                        "current": 4,
                        "total": 4,
                        "endOfPeriod": False
                    },
                    "arena": {
                        "name": None,
                        "city": None,
                        "state": None,
                        "country": None
                    },
                    "teams": {
                        "visitors": {
                            "id": 16,
                            "name": "LA Clippers",
                            "nickname": "Clippers",
                            "code": "LAC",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/d/d6/Los_Angeles_Clippers_logo_2010.png"
                        },
                        "home": {
                            "id": 6,
                            "name": "Chicago Bulls",
                            "nickname": "Bulls",
                            "code": "CHI",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/d/d1/Bulls_de_Chicago_logo.svg/1200px-Bulls_de_Chicago_logo.svg.png"
                        }
                    },
                    "scores": {
                        "visitors": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "20",
                                "34",
                                "31",
                                "23"
                            ],
                            "points": 108
                        },
                        "home": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "32",
                                "26",
                                "26",
                                "19"
                            ],
                            "points": 103
                        }
                    },
                    "officials": [],
                    "timesTied": None,
                    "leadChanges": None,
                    "nugget": None
                },
                {
                    "id": 1005,
                    "league": "standard",
                    "season": 2022,
                    "date": {
                        "start": "2023-02-01T01:00:00.000Z",
                        "end": None,
                        "duration": None
                    },
                    "stage": 2,
                    "status": {
                        "clock": None,
                        "halftime": False,
                        "short": 3,
                        "long": "Finished"
                    },
                    "periods": {
                        "current": 4,
                        "total": 4,
                        "endOfPeriod": False
                    },
                    "arena": {
                        "name": None,
                        "city": None,
                        "state": None,
                        "country": None
                    },
                    "teams": {
                        "visitors": {
                            "id": 5,
                            "name": "Charlotte Hornets",
                            "nickname": "Hornets",
                            "code": "CHA",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/f/f3/Hornets_de_Charlotte_logo.svg/1200px-Hornets_de_Charlotte_logo.svg.png"
                        },
                        "home": {
                            "id": 21,
                            "name": "Milwaukee Bucks",
                            "nickname": "Bucks",
                            "code": "MIL",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/3/34/Bucks2015.png"
                        }
                    },
                    "scores": {
                        "visitors": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "27",
                                "37",
                                "26",
                                "25"
                            ],
                            "points": 115
                        },
                        "home": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "34",
                                "30",
                                "33",
                                "27"
                            ],
                            "points": 124
                        }
                    },
                    "officials": [],
                    "timesTied": None,
                    "leadChanges": None,
                    "nugget": None
                },
                {
                    "id": 1006,
                    "league": "standard",
                    "season": 2022,
                    "date": {
                        "start": "2023-02-01T03:00:00.000Z",
                        "end": None,
                        "duration": None
                    },
                    "stage": 2,
                    "status": {
                        "clock": None,
                        "halftime": False,
                        "short": 3,
                        "long": "Finished"
                    },
                    "periods": {
                        "current": 4,
                        "total": 4,
                        "endOfPeriod": False
                    },
                    "arena": {
                        "name": None,
                        "city": None,
                        "state": None,
                        "country": None
                    },
                    "teams": {
                        "visitors": {
                            "id": 23,
                            "name": "New Orleans Pelicans",
                            "nickname": "Pelicans",
                            "code": "NOP",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/2/21/New_Orleans_Pelicans.png/200px-New_Orleans_Pelicans.png"
                        },
                        "home": {
                            "id": 9,
                            "name": "Denver Nuggets",
                            "nickname": "Nuggets",
                            "code": "DEN",
                            "logo": "https://upload.wikimedia.org/wikipedia/fr/thumb/3/35/Nuggets_de_Denver_2018.png/180px-Nuggets_de_Denver_2018.png"
                        }
                    },
                    "scores": {
                        "visitors": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "35",
                                "25",
                                "24",
                                "29"
                            ],
                            "points": 113
                        },
                        "home": {
                            "win": 0,
                            "loss": 0,
                            "series": {
                                "win": 0,
                                "loss": 0
                            },
                            "linescore": [
                                "31",
                                "26",
                                "36",
                                "29"
                            ],
                            "points": 122
                        }
                    },
                    "officials": [],
                    "timesTied": None,
                    "leadChanges": None,
                    "nugget": None
                }
            ]
        }

        response_game_id_list = [1000, 1001, 1003, 1005, 1006]

        game_id_list = db_insert_game(sample_game_data)
        game_data = Game.objects.all()
        self.assertEqual(game_data.count(), 5) # 5件データが挿入されているか確認
        self.assertEqual(game_id_list, response_game_id_list)
