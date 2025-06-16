import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
import threading
import json

from charts.line_trend import create_line_chart
from charts.pie_chart import create_pie_chart
from charts.weather_map import create_weather_map
from charts.wordcloud_chart import create_weather_wordcloud
from charts.avg_tempchart import create_avg_temp_bar_chart
from charts.wind_chart import create_wind_direction_chart

from spider.weather_spider import update_weather_csv

app = Flask(__name__)

# 点赞相关配置
LIKE_FILE = 'likes.json'
like_lock = threading.Lock()  # 点赞锁
UPDATE_TIMESTAMP_FILE = 'last_update.txt'
update_lock = threading.Lock()  # 更新锁

# 初始化点赞数据
if not os.path.exists(LIKE_FILE):
    with like_lock:
        with open(LIKE_FILE, 'w') as f:
            json.dump({'likes': 0}, f)

def read_likes():
    with like_lock:
        with open(LIKE_FILE, 'r') as f:
            return json.load(f)['likes']

def write_likes(count):
    with like_lock:
        with open(LIKE_FILE, 'w') as f:
            json.dump({'likes': count}, f)

@app.route('/like', methods=['POST'])
def like():
    likes = read_likes() + 1
    write_likes(likes)
    return jsonify({'likes': likes})

@app.route('/get_likes', methods=['GET'])
def get_likes():
    return jsonify({'likes': read_likes()})

def need_update():
    if not os.path.exists(UPDATE_TIMESTAMP_FILE):
        return True
    try:
        with open(UPDATE_TIMESTAMP_FILE, 'r') as f:
            last_update_str = f.read().strip()
        last_update = datetime.fromisoformat(last_update_str)
    except Exception:
        return True
    return datetime.now() - last_update > timedelta(hours=24)

def record_update_time():
    with open(UPDATE_TIMESTAMP_FILE, 'w') as f:
        f.write(datetime.now().isoformat())

def background_update():
    with update_lock:
        print("后台线程开始更新天气数据...")
        try:
            update_weather_csv()
            record_update_time()
            print("天气数据更新完成")
        except Exception as e:
            print(f"更新天气数据出错: {e}")

@app.route('/')
def index():
    if need_update():
        if update_lock.acquire(blocking=False):
            try:
                threading.Thread(target=background_update, daemon=True).start()
                print("已启动后台线程更新数据")
            finally:
                update_lock.release()
        else:
            print("已有更新线程在运行，跳过启动新线程")
    else:
        print("数据已是最新，直接使用缓存")

    # 生成图表
    line_chart = create_line_chart()
    pie_chart = create_pie_chart()
    weather_map = create_weather_map()
    wordcloud = create_weather_wordcloud()
    avg_tempchart = create_avg_temp_bar_chart()
    wind_chart = create_wind_direction_chart()

    return render_template(
        'index.html',
        line_chart=line_chart.render_embed(),
        pie_chart=pie_chart.render_embed(),
        weather_map=weather_map.render_embed(),
        wordcloud=wordcloud.render_embed(),
        avg_tempchart=avg_tempchart.render_embed(),
        wind_chart=wind_chart.render_embed()
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)