import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

def create_line_chart():
    # 读取数据
    df = pd.read_csv('city-weather.csv')

    # 日期处理
    df['日期'] = df['日期'].str.extract(r'(\d{4}-\d{2}-\d{2})')[0]
    df['日期'] = pd.to_datetime(df['日期'])

    # 温度转换
    df['最高温度'] = df['最高温度'].str.replace('°', '', regex=False).astype(float)
    df['最低温度'] = df['最低温度'].str.replace('°', '', regex=False).astype(float)

    # 日期排序
    df = df.sort_values(by='日期')

    # 获取所有日期和城市
    dates = df['日期'].dt.strftime('%Y-%m-%d').unique().tolist()
    cities = df['城市'].unique()

    # 创建图表
    line = Line(init_opts=opts.InitOpts(
        width="1200px",
        height="600px",
        bg_color="rgba(10, 25, 47, 0.9)"
    ))

    line.add_xaxis(dates)

    for city in cities:
        city_data = df[df['城市'] == city][['日期', '最高温度', '最低温度']].set_index('日期')
        city_data = city_data.reindex(pd.to_datetime(dates))  # 补全缺失日期
        high = city_data['最高温度'].tolist()
        low = city_data['最低温度'].tolist()

        line.add_yaxis(
            f"{city} - 最高温",
            high,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )
        line.add_yaxis(
            f"{city} - 最低温",
            low,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )

    white_text_style = opts.TextStyleOpts(color="#ffffff", font_weight="bold")

    # 设置全局样式和提示框
    line.set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            background_color="rgba(50,50,50,0.8)",
            border_color="#aaa",
            border_width=1,
            textstyle_opts=white_text_style
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            name="日期",
            axislabel_opts=opts.LabelOpts(color="#ffffff"),
            name_textstyle_opts=white_text_style,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#ffffff")
            )
        ),
        yaxis_opts=opts.AxisOpts(
            name="温度 (°C)",
            axislabel_opts=opts.LabelOpts(color="#ffffff"),
            name_textstyle_opts=white_text_style,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#ffffff")
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(color="rgba(255,255,255,0.1)")
            )
        ),
        legend_opts=opts.LegendOpts(
            type_="scroll",
            pos_bottom="50px",
            orient="horizontal",
            item_gap=10,
            textstyle_opts=white_text_style
        )
    )

    # 设置图表边距
    line.options["grid"] = {
        "bottom": "150px",
        "top": "60px"
    }

    return line

