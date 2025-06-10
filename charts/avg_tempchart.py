import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

def create_avg_temp_bar_chart():
    df = pd.read_csv('city-weather.csv')

    # 处理温度数据，去掉“°”转float
    df['最高温度'] = df['最高温度'].str.replace('°', '').astype(float)
    df['最低温度'] = df['最低温度'].str.replace('°', '').astype(float)

    # 计算各城市平均最高温和平均最低温
    city_avg = df.groupby('城市').agg({'最高温度': 'mean', '最低温度': 'mean'}).reset_index()

    cities = city_avg['城市'].tolist()
    avg_high = city_avg['最高温度'].round(2).tolist()
    avg_low = city_avg['最低温度'].round(2).tolist()

    bar = (
        Bar(init_opts=opts.InitOpts(width="800px", height="400px"))
        .add_xaxis(cities)
        .add_yaxis("平均最高温 (°C)", avg_high, color="#d14a61")
        .add_yaxis("平均最低温 (°C)", avg_low, color="#5793f3")
        .set_global_opts(
            # title_opts=opts.TitleOpts(title="各城市平均最高气温与最低气温"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
            xaxis_opts=opts.AxisOpts(name="城市", axislabel_opts=opts.LabelOpts(rotate=30)),
            yaxis_opts=opts.AxisOpts(name="温度 (°C)"),
            legend_opts=opts.LegendOpts(pos_top="5%")
        )
    )
    return bar
