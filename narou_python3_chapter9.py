# 発展2：指定した期間における総合評価ポイントの分布を図示する

import datetime
import gzip
import json
import math
import pprint
import statistics
from time import sleep

import matplotlib.pyplot as plt
import requests


# 関数
def narou_api(url, params, all_bytes):
    r = requests.get(url, params=params)
    bytes = r.headers["Content-Length"]
    data = r.content
    data = gzip.decompress(data)
    data = json.loads(data)
    all_bytes += int(bytes)
    sleep(1)
    return data, all_bytes


# 本体
url = "https://api.syosetu.com/novelapi/api/"
params = {}
all_bytes = 0

# 出力GETパラメータの設定
params.update([("gzip", 5), ("out", "json"), ("lim", 1)])

# 条件抽出GETパラメータの設定
start_dt = datetime.datetime(
    2025, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
)
end_dt = datetime.datetime(
    2026, 1, 1, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
)

# UNIX時間に変換し、小数点以下切り捨て
start_uni = math.floor(start_dt.timestamp())
end_uni = math.floor(end_dt.timestamp())

params.update([("lastup", str(start_uni) + "-" + str(end_uni)), ("type", "t")])

# ofパラメータの設定
params.update([("of", "n-gp")])

# 指定された期間の作品件数を取得
data, all_bytes = narou_api(url, params, all_bytes)
allcount = data[0]["allcount"]

# 何分割するか
division_count = math.ceil(allcount / 1500)

# 時間を分割
division_time = (end_uni - start_uni) // division_count
get_start_time = start_uni
get_end_time = start_uni + division_time

all_datas_raw = []
false_time = []
start_datetime = start_dt.strftime("%Y/%m/%d %H:%M")
end_datetime = end_dt.strftime("%Y/%m/%d %H:%M")

while get_end_time <= end_uni:
    params.update(
        [("lastup", str(get_start_time) + "-" + str(get_end_time)), ("lim", 1)]
    )
    data, all_bytes = narou_api(url, params, all_bytes)
    get_count = data[0]["allcount"]

    if get_count >= 2000:
        division_count2 = math.ceil(get_count / 1500)
        division_time2 = (get_end_time - get_start_time) // division_count
        get_end_time = get_start_time + division_time2
        continue

    # 作品情報の取得
    stn = 1
    data_tmp = []
    while stn < get_count:
        params.update([("lim", 500), ("st", stn)])
        data, all_bytes = narou_api(url, params, all_bytes)
        del data[0]
        data_tmp.extend(data)
        stn += 500

    get_start_datetime = datetime.datetime.fromtimestamp(
        get_start_time, datetime.timezone(datetime.timedelta(hours=9))
    )
    get_start_datetime = get_start_datetime.strftime("%Y/%m/%d %H:%M")
    get_end_datetime = datetime.datetime.fromtimestamp(
        get_end_time, datetime.timezone(datetime.timedelta(hours=9))
    )
    get_end_datetime = get_end_datetime.strftime("%Y/%m/%d %H:%M")

    all_datas_raw.extend(data_tmp)
    if get_count == len(data_tmp):
        pass
    else:
        false_time.append(
            f"{get_start_datetime}>>>{get_end_datetime}：{get_count - len(data_tmp)}"
        )

    print(
        f"\r取得中：{start_datetime}：{get_start_datetime}>>>{get_end_datetime}：{end_datetime}",
        end="",
    )

    # 取得期間を更新
    if get_end_time >= end_uni:
        break
    get_start_time = get_end_time
    get_end_time = get_end_time + division_time
    if get_end_time >= end_uni:
        get_end_time = end_uni

# データの重複削除
all_get_count = len(all_datas_raw)
tmp = []
all_datas = [x for x in all_datas_raw if x not in tmp and not tmp.append(x)]

print("\n取得完了")

# きちんと取得できているか確認
get_count_works = len(all_datas)
if allcount == get_count_works:
    print("一致している")
else:
    print("一致していない")
    print(f"全期間のHIT数：{allcount}")
    print(f"取得した数：{get_count_works}")
    print(f"差：{allcount - get_count_works}")
    pprint.pprint(false_time)
print()

# 利用制限の確認
print(f"取得件数：{all_get_count}")
multiplier = math.floor(math.log(all_bytes, 1024))
size = round(all_bytes / 1024**multiplier, 2)
units = ["B", "KB", "MB", "GB", "TB"]
print(f"転送量：{size}{units[multiplier]}")
print()

# 総合評価ポイントのデータを抽出
all_global_point = []
for i in all_datas:
    all_global_point.append(i["global_point"])

# データの基本統計量を確認
print(f"作品数：{len(all_global_point)}")
print(f"最大値：{max(all_global_point)}")
print(f"最小値：{min(all_global_point)}")
print(f"平均値：{statistics.mean(all_global_point):.1f}")
print(f"中央値：{statistics.median(all_global_point)}")
print(f"最頻値：{statistics.mode(all_global_point):.1f}")
print(f"標準偏差：{statistics.stdev(all_global_point):.1f}")
print()

# ヒストグラムを表示
bin_count = int(math.log2(len(all_global_point)) + 1)
plt.hist(all_global_point, bins=bin_count)
plt.show()

# 指定したポイントの位置を確認
global_point = 1
if global_point not in all_global_point:
    all_global_point.append(global_point)
all_global_point.sort()
rank = [i for i, x in enumerate(all_global_point) if x == global_point]
print(f"下から{statistics.median(rank) + 1}番目")
rank_ratio = (statistics.median(rank) + 1) / len(all_global_point) * 100
print(f"下から{rank_ratio:.1f}%")
deviation = (global_point - statistics.mean(all_global_point)) / statistics.pstdev(
    all_global_point
) * 10 + 50
print(f"偏差値：{deviation:.1f}")

print()
print("動作終了")
