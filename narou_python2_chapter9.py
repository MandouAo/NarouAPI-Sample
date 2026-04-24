# 発展1：条件を満たす作品の情報をダウンロードする
import datetime
import gzip
import json

import requests

# APIのURL
ulr = "https://api.syosetu.com/novelapi/api/"

params = {}

# 出力GETパラメータの設定
params.update([("gzip", 5), ("out", "json"), ("lim", 3), ("order", "hyoka")])

# 条件抽出GETパラメータの設定

# 検索する期間を指定する
start_dt = datetime.datetime(
    2025, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
)
end_dt = datetime.datetime(
    2026, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
)

# floatなのでint→strに変換
start_uni = str(int(start_dt.timestamp()))
end_uni = str(int(end_dt.timestamp()))

params.update([("lastup", start_uni + "-" + end_uni), ("biggenre", "1-2")])

# ofパラメータの設定
params.update([("of", "t-n-k-nt")])

# APIの実行
r = requests.get(ulr, params=params)
print(r.url)

# 転送量の表示
bytes = r.headers["Content-Length"]
print("転送量：" + bytes + "B")

# 返ってきたデータをJSONファイルに書き込み
data = r.content
data = gzip.decompress(data)
data = json.loads(data)
with open("NarouAPI.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
