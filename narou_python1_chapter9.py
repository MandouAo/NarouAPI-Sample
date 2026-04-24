# 基本：条件を指定して検索結果を3件表示する
import gzip
import json
import pprint

import requests

# APIのURL
ulr = "https://api.syosetu.com/novelapi/api/"

params = {}

# 出力GETパラメータの設定
params.update([("gzip", 5), ("out", "json"), ("lim", 3), ("order", "yearlypoint")])

# 条件抽出GETパラメータの設定
params.update([("istt", 1), ("time", "-30"), ("type", "ter")])

# ofパラメータの設定
params.update([("of", "t-w-s-k-ti-gp")])

# APIの実行
r = requests.get(ulr, params=params)
print(r.url)

# 返ってきたデータの表示
data = r.content
data = gzip.decompress(data)
data = json.loads(data)
pprint.pprint(data)
