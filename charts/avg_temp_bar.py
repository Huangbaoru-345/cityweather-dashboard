import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
def avg_temp_bar_chart():
    df = pd.read_csv('city-weather.csv')
    cities = ['广州市', '深圳市', '重庆市', '北京市', '杭州市', '武汉市', '南京市', '上海市']
    df['最高温度'] = df['最高温度'].str.replace('°', '', regex=False).astype(float)
    df_filtered = df[df['城市'].isin(cities)]

    avg_high_temp = df_filtered.groupby('城市')['最高温度'].mean().reset_index()
    avg_high_temp = avg_high_temp.sort_values(by='最高温度', ascending=False)

    bar = (
        Bar()
        .add_xaxis(avg_high_temp['城市'].tolist())
        .add_yaxis(
            "平均最高温度",
            avg_high_temp['最高温度'].round(1).tolist(),
            itemstyle_opts=opts.ItemStyleOpts(color="#ff7f50")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="8个城市的平均最高温度", pos_left="20%"),
            xaxis_opts=opts.AxisOpts(name="城市"),
            yaxis_opts=opts.AxisOpts(name="温度（℃）"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )

    return bar  # ✅ 返回图表对象，后续加入 Page
