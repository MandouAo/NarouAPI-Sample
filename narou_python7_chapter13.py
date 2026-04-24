# なろう殿堂入りAPI
import gzip
import json
import pprint

import requests

# APIのURL
ulr = "https://api.syosetu.com/rank/rankin/"

params = {}

# GETパラメータの設定
params.update([("gzip", 5), ("out", "json"), ("ncode", "N2710DB")])

# APIの実行
r = requests.get(ulr, params=params)
print(r.url)

# 返ってきたデータの表示
data = r.content
data = gzip.decompress(data)
data = json.loads(data)
pprint.pprint(data)
