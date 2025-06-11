import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

def create_pie_chart():
    df = pd.read_csv('city-weather.csv')

    sunny_counts = df[df['天气'].str.contains('晴')]['城市'].value_counts()
    data_pair = list(zip(sunny_counts.index.tolist(), sunny_counts.tolist()))

    pie = Pie(init_opts=opts.InitOpts(
        width="700px",
        height="500px",
        bg_color="rgba(10, 25, 47, 0.9)"  # 深色背景
    ))

    pie.add(
        "晴天天数占比",  # 这个参数不能省略
        data_pair,
        radius=["40%", "70%"],
        center=["50%", "60%"],
        label_opts=opts.LabelOpts(
            formatter="{b}: {d}%",
            color="#ffffff",
            font_weight="bold"
        )
    )

    pie.set_global_opts(
        title_opts=opts.TitleOpts(
            # title="各城市晴天占比",
            pos_top="2%",
            title_textstyle_opts=opts.TextStyleOpts(
                color="#ffffff",
                font_weight="bold"
            )
        ),
        legend_opts=opts.LegendOpts(
            orient="horizontal",
            pos_top="5%",
            pos_left="center",
            item_gap=20,
            textstyle_opts=opts.TextStyleOpts(
                color="#ffffff",
                font_weight="bold"
            )
        )
    )

    pie.set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            formatter="{b}: {d}%",
            background_color="transparent",  # 透明背景去掉白框
            textstyle_opts=opts.TextStyleOpts(
                color="#ffffff"
            )
        )
    )

    return pie
