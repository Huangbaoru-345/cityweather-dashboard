import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

def create_line_chart():
    df = pd.read_csv('city-weather.csv')
    df['日期'] = pd.to_datetime(df['日期'].str.extract(r'(\d{4}-\d{2}-\d{2})')[0])
    df['最高温度'] = df['最高温度'].str.replace('°', '').astype(float)
    df['最低温度'] = df['最低温度'].str.replace('°', '').astype(float)
    df = df.sort_values('日期')

    dates = df['日期'].dt.strftime('%Y-%m-%d').unique().tolist()
    cities = df['城市'].unique()

    line = Line(init_opts=opts.InitOpts(width="1200px", height="600px", bg_color="rgba(10, 25, 47, 0.9)"))
    line.add_xaxis(dates)

    for city in cities:
        city_data = df[df['城市'] == city].sort_values('日期')
        line.add_yaxis(f"{city} - 最高温", city_data['最高温度'].tolist(), is_smooth=True, label_opts=opts.LabelOpts(is_show=False))
        line.add_yaxis(f"{city} - 最低温", city_data['最低温度'].tolist(), is_smooth=True, label_opts=opts.LabelOpts(is_show=False))

    white_text_style = opts.TextStyleOpts(color="#fff", font_weight="bold")

    line.set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", textstyle_opts=white_text_style),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            name="日期",
            axislabel_opts=opts.LabelOpts(color="#fff"),
            name_textstyle_opts=white_text_style,
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#fff")),
        ),
        yaxis_opts=opts.AxisOpts(
            name="温度 (°C)",
            axislabel_opts=opts.LabelOpts(color="#fff"),
            name_textstyle_opts=white_text_style,
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#fff")),
            splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(color="rgba(255,255,255,0.1)")),
        ),
        legend_opts=opts.LegendOpts(type_="scroll", pos_bottom="50px", orient="horizontal", item_gap=10, textstyle_opts=white_text_style)
    )

    line.options["grid"] = {"bottom": "150px", "top": "60px"}

    return line
