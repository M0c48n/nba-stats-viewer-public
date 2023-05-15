import http.client
import json


# 共通処理
def convert_to_json(conn):
    res = conn.getresponse()
    tmp = res.read()
    data = json.loads(tmp.decode('utf-8'))

    return data
