import os
from datetime import datetime, timedelta
from flask import Flask, render_template
from charts.line_trend import create_line_chart  # 折线图
from charts.pie_chart import create_pie_chart     # 饼图
from charts.weather_map import create_weather_map
from charts.wordcloud_chart import create_weather_wordcloud
from charts.avg_tempchart import create_avg_temp_bar_chart
from charts.wind_chart import create_wind_direction_chart
from spider.weather_spider import update_weather_csv

app = Flask(__name__)

UPDATE_TIMESTAMP_FILE = 'last_update.txt'  # 记录上次更新时间的文件

def need_update():
    if not os.path.exists(UPDATE_TIMESTAMP_FILE):
        return True
    with open(UPDATE_TIMESTAMP_FILE, 'r') as f:
        last_update_str = f.read().strip()
    try:
        last_update = datetime.fromisoformat(last_update_str)
    except Exception:
        return True
    return datetime.now() - last_update > timedelta(hours=24)  # 超过24小时需更新

def record_update_time():
    with open(UPDATE_TIMESTAMP_FILE, 'w') as f:
        f.write(datetime.now().isoformat())

@app.route('/')
def index():
    if need_update():
        print("开始更新天气数据...")
        update_weather_csv()
        record_update_time()
    else:
        print("使用缓存的天气数据，无需更新")

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
