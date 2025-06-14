import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

def create_pie_chart():
    df = pd.read_csv('city-weather.csv')

    # 获取所有城市（保持顺序）
    city_list = df['城市'].unique()

    # 统计每个城市的“晴”天数
    sunny_counts = df[df['天气'].str.contains('晴', na=False)]['城市'].value_counts()

    # 保证所有城市都在统计中，缺失的城市用 0 填充
    sunny_counts = sunny_counts.reindex(city_list, fill_value=0)

    # 转为 (城市, 晴天数) 的列表
    data_pair = list(zip(sunny_counts.index.tolist(), sunny_counts.tolist()))

    # 创建饼图对象
    pie = Pie(init_opts=opts.InitOpts(
        width="700px",
        height="500px",
        bg_color="rgba(10, 25, 47, 0.9)"  # 深色背景
    ))

    pie.add(
        "晴天天数占比",
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
            background_color="transparent",
            textstyle_opts=opts.TextStyleOpts(
                color="#ffffff"
            )
        )
    )

    return pie
