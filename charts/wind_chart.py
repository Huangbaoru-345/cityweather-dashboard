import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

def create_wind_direction_chart():
    # 读取数据
    df = pd.read_csv('city-weather.csv')

    # 按城市和风向分组计数，生成透视表
    group = df.groupby(['城市', '风向']).size().unstack(fill_value=0)
    cities = group.index.tolist()
    wind_dirs = group.columns.tolist()

    # 全局字体样式，浅蓝色
    text_style = {
        "color": "#e6f1ff",
        "fontSize": 12,
        "fontFamily": "'Roboto', 'Microsoft YaHei', sans-serif"
    }

    # 初始化柱状图，设置半透明深蓝背景
    bar = Bar(init_opts=opts.InitOpts(
        width="900px",
        height="500px",
        bg_color="rgba(10, 25, 47, 0.1)"
    ))

    # 设置X轴（城市名）
    bar.add_xaxis(cities)

    # 添加风向数据堆叠柱状图
    for wind_dir in wind_dirs:
        bar.add_yaxis(
            series_name=wind_dir,
            y_axis=group[wind_dir].tolist(),
            stack="stack1",  # 堆叠
            label_opts=opts.LabelOpts(
                color="#ffffff",  # 堆叠柱内部白色标签
                position="inside",
                font_size=10
            )
        )

    # 设置全局选项：坐标轴、图例、提示框等
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(
            name="城市",
            name_textstyle_opts=text_style,
            axislabel_opts=opts.LabelOpts(
                rotate=30,
                color="#e6f1ff",
                font_size=11
            ),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="rgba(0, 247, 255, 0.5)")
            ),
            splitline_opts=opts.SplitLineOpts(is_show=False)
        ),
        yaxis_opts=opts.AxisOpts(
            name="出现次数",
            name_textstyle_opts=text_style,
            axislabel_opts=opts.LabelOpts(color="#e6f1ff"),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="rgba(0, 247, 255, 0.5)")
            ),
            splitline_opts=opts.SplitLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="rgba(0, 247, 255, 0.1)")
            )
        ),
        legend_opts=opts.LegendOpts(
            pos_top="1%",
            textstyle_opts=text_style,
            item_width=25,
            item_height=14,
            item_gap=20,
            inactive_color="rgba(200, 200, 200, 0.4)"
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="shadow",
            background_color="rgba(10, 25, 47, 0.9)",
            border_color="rgba(0, 247, 255, 0.5)",
            textstyle_opts=opts.TextStyleOpts(
                color="#ffffff",
                font_size=14
            )
        )
    )

    # 自定义网格边距，调整图表位置
    bar.options['grid'] = {
        "top": "35%",
        "left": "5%",
        "right": "5%",
        "bottom": "15%"
    }

    return bar
