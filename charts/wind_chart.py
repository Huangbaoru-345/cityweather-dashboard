import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

def create_wind_direction_chart():
    df = pd.read_csv('city-weather.csv')

    # 按城市和风向分组计数，unstack变成宽表，缺失补0
    group = df.groupby(['城市', '风向']).size().unstack(fill_value=0)

    cities = group.index.tolist()          # 城市名称列表
    wind_dirs = group.columns.tolist()     # 风向列表

    bar = Bar(init_opts=opts.InitOpts(width="900px", height="500px"))
    bar.add_xaxis(cities)

    # 添加每个风向的堆叠数据
    for wind_dir in wind_dirs:
        bar.add_yaxis(
            series_name=wind_dir,
            y_axis=group[wind_dir].tolist(),
            stack="stack1"  # 同一堆叠组
        )

    bar.set_global_opts(
    # title_opts=opts.TitleOpts(title="按城市分类的风向频次分析"),
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
    xaxis_opts=opts.AxisOpts(name="城市", axislabel_opts={"rotate": 30}),
    yaxis_opts=opts.AxisOpts(name="出现次数"),
    legend_opts=opts.LegendOpts(pos_top="1%", padding=[10, 0, 0, 0], item_gap=20),
    )

    bar.set_series_opts(
    label_opts=opts.LabelOpts(),
    # 这里GridOpts不是series_opts的参数，不用放这里，下面是个技巧
    )

    bar.options['grid'] = {"top": "35%"}  # 直接改options字典，top留空格

    return bar
