from flask import Flask, render_template
from charts.line_trend import create_line_chart  # 折线图
from charts.pie_chart import create_pie_chart     # 饼图
from charts.weather_map import create_weather_map
from charts.wordcloud_chart import create_weather_wordcloud
from charts.avg_tempchart import create_avg_temp_bar_chart
from charts.wind_chart import create_wind_direction_chart
app = Flask(__name__)

@app.route('/')
def index():
    line_chart = create_line_chart()     # ✅ 使用正确的函数名
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
        wordcloud = wordcloud.render_embed(),
        avg_tempchart = avg_tempchart.render_embed(),
        wind_chart = wind_chart.render_embed()
    )

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

