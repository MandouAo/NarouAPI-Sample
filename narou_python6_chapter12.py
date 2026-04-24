# なろう小説ランキングAPI
import gzip
import json
import pprint

import requests

# APIのURL
ulr = "https://api.syosetu.com/rank/rankget/"

params = {}

# GETパラメータの設定
params.update([("gzip", 5), ("out", "json"), ("rtype", "20260101-q")])

# APIの実行
r = requests.get(ulr, params=params)
print(r.url)

# 返ってきたデータの表示
data = r.content
data = gzip.decompress(data)
data = json.loads(data)
pprint.pprint(data)
