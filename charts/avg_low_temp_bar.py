import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

def avg_low_temp_bar_chart():
    import pandas as pd
    from pyecharts.charts import Bar
    from pyecharts import options as opts

    df = pd.read_csv('city-weather.csv')
    print(df.head())  # 调试输出看看数据

    df['最低温度'] = df['最低温度'].str.replace('°', '', regex=False).astype(float)
    cities = ['广州市', '深圳市', '重庆市', '北京市', '杭州市', '武汉市', '南京市', '上海市']
    df_filtered = df[df['城市'].isin(cities)]

    print(df_filtered)  # 再调试确认过滤后的数据

    avg_low_temp = df_filtered.groupby('城市')['最低温度'].mean().reset_index()
    avg_low_temp = avg_low_temp.sort_values(by='最低温度', ascending=False)
    print(avg_low_temp)  # 平均温度确认

    bar = (
        Bar()
        .add_xaxis(avg_low_temp['城市'].tolist())
        .add_yaxis("平均最低温度", avg_low_temp['最低温度'].round(1).tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="8个城市的平均最低温度", pos_left="20%"),
            xaxis_opts=opts.AxisOpts(name="城市"),
            yaxis_opts=opts.AxisOpts(name="温度（℃）"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return bar
