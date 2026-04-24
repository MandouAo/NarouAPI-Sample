# なろうユーザ検索API
import gzip
import json
import pprint

import requests

# APIのURL
ulr = "https://api.syosetu.com/userapi/api/"

params = {}

# 出力GETパラメータの設定
params.update([("gzip", 5), ("out", "json"), ("lim", 3), ("order", "sumglobalpoint")])

# 条件抽出GETパラメータの設定
params.update([("minnovel", 2)])

# ofパラメータの設定
params.update([("of", "n-y-nc-sg")])

# APIの実行
r = requests.get(ulr, params=params)
print(r.url)

# 返ってきたデータの表示
data = r.content
data = gzip.decompress(data)
data = json.loads(data)
pprint.pprint(data)
