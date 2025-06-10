import pandas as pd
from pyecharts.charts import Line, Tab
from pyecharts import options as opts

def line_temperature_chart():
    df = pd.read_csv('city-weather.csv')

    cities = ['广州市', '深圳市', '重庆市', '北京市', '杭州市', '武汉市', '南京市', '上海市']
    
    # 清洗通用字段
    df['日期'] = df['日期'].str.extract(r'(\d{4}-\d{2}-\d{2})')
    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
    df['最高温度'] = pd.to_numeric(df['最高温度'].str.replace('°', ''), errors='coerce')
    df['最低温度'] = pd.to_numeric(df['最低温度'].str.replace('°', ''), errors='coerce')

    tab = Tab()

    for city in cities:
        city_df = df[df['城市'] == city].sort_values(by='日期').copy()

        dates = city_df['日期'].dt.strftime('%Y-%m-%d').tolist()
        highs = city_df['最高温度'].tolist()
        lows = city_df['最低温度'].tolist()

        line = (
            Line()
            .add_xaxis(dates)
            .add_yaxis("最高温度", highs, is_smooth=True)
            .add_yaxis("最低温度", lows, is_smooth=True)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"{city}气温变化趋势", pos_left="center"),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, axislabel_opts={"rotate": 45}),
                yaxis_opts=opts.AxisOpts(name="温度（°C）"),
                legend_opts=opts.LegendOpts(pos_top="5%"),
            )
        )

        tab.add(line, city)

    return tab