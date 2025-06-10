import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

def weather_pie_chart(city):
    df = pd.read_csv('city-weather.csv')
    city_df = df[df['城市'] == city].copy()
    weather_counts = city_df['天气'].value_counts().to_dict()
    data_list = list(weather_counts.items())

    pie = (
        Pie(init_opts=opts.InitOpts(width="800px"))  # 这里设置初始宽度
        .add("", data_list)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{city}天气分布"),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_top="15%",
                pos_left="2%"
            )
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    return pie