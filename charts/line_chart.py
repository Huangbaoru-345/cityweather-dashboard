import pandas as pd
from pyecharts.charts import Line, Tab
from pyecharts import options as opts

def line_temperature_chart():
    df = pd.read_csv('city-weather.csv')

    cities = ['广州市', '深圳市', '重庆市', '北京市', '杭州市', '武汉市', '南京市', '上海市']

    # 清洗字段
    df['日期'] = df['日期'].str.extract(r'(\d{4}-\d{2}-\d{2})')
    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
    df['最高温度'] = pd.to_numeric(df['最高温度'].str.replace('°', ''), errors='coerce')
    df['最低温度'] = pd.to_numeric(df['最低温度'].str.replace('°', ''), errors='coerce')

    # 字体样式：白色或亮蓝色，更清晰
    label_style = opts.LabelOpts(
        color="#ffffff",  # 白色字体
        font_weight="bold"
    )

    text_style = opts.TextStyleOpts(
        color="#ffffff",  # 白色字体
        font_weight="bold",
        font_family="'Microsoft YaHei', sans-serif"
    )

    axis_line_style = opts.AxisLineOpts(
        linestyle_opts=opts.LineStyleOpts(color="#ffffff")  # 白色坐标轴线
    )

    tab = Tab()

    for city in cities:
        city_df = df[df['城市'] == city].sort_values(by='日期').copy()

        dates = city_df['日期'].dt.strftime('%Y-%m-%d').tolist()
        highs = city_df['最高温度'].tolist()
        lows = city_df['最低温度'].tolist()

        line = (
            Line(init_opts=opts.InitOpts(
                width="900px",
                height="500px",
                bg_color="rgba(10, 25, 47, 0.9)"  # 深蓝背景
            ))
            .add_xaxis(dates)
            .add_yaxis("最高温度", highs, is_smooth=True, label_opts=label_style)
            .add_yaxis("最低温度", lows, is_smooth=True, label_opts=label_style)
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{city}气温变化趋势",
                    pos_left="center",
                    title_textstyle_opts=text_style
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    textstyle_opts=text_style
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    boundary_gap=False,
                    axislabel_opts=opts.LabelOpts(color="#ffffff"),  # x轴字体设白
                    axisline_opts=axis_line_style
                ),
                yaxis_opts=opts.AxisOpts(
                    name="温度（°C）",
                    axislabel_opts=opts.LabelOpts(color="#ffffff"),  # y轴字体设白
                    name_textstyle=opts.TextStyleOpts(color="#ffffff"),
                    axisline_opts=axis_line_style,
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True,
                        linestyle_opts=opts.LineStyleOpts(color="#004466")
                    )
                ),
                legend_opts=opts.LegendOpts(
                    pos_top="5%",
                    textstyle_opts=text_style
                ),
            )
        )

        tab.add(line, city)

    return tab
