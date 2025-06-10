import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

def create_line_chart():
    # 读取数据
    df = pd.read_csv('city-weather.csv')

    # 提取日期部分，转换为datetime格式，方便排序和格式化显示
    df['日期'] = df['日期'].str.extract(r'(\d{4}-\d{2}-\d{2})')
    df['日期'] = pd.to_datetime(df['日期'])

    # 清洗温度数据，去掉‘°’，转换为浮点数
    df['最高温度'] = df['最高温度'].str.replace('°', '').astype(float)
    df['最低温度'] = df['最低温度'].str.replace('°', '').astype(float)

    # 按日期排序
    df = df.sort_values(by='日期')

    # 获取唯一日期和城市列表
    dates = df['日期'].dt.strftime('%Y-%m-%d').unique().tolist()
    cities = df['城市'].unique()

    # 初始化折线图，设置宽高
    line = Line(init_opts=opts.InitOpts(width="1200px", height="600px"))

    # 添加X轴（日期）
    line.add_xaxis(dates)

    # 添加各城市的最高温和最低温曲线，平滑显示，隐藏标签避免图表过于拥挤
    for city in cities:
        city_data = df[df['城市'] == city].sort_values(by='日期')
        line.add_yaxis(
            f"{city} - 最高温", 
            city_data['最高温度'].tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )
        line.add_yaxis(
            f"{city} - 最低温",
            city_data['最低温度'].tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )

    # 设置全局配置
    line.set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis"),  # 鼠标悬浮显示X轴对应所有数据
        xaxis_opts=opts.AxisOpts(type_="category", name="日期"),
        yaxis_opts=opts.AxisOpts(name="温度 (°C)"),
        legend_opts=opts.LegendOpts(
            type_="scroll",            # 图例超过显示区域时可滚动
            pos_bottom="50px",         # 图例距离底部50px，离图表主体有间距
            orient="horizontal",       # 水平排列图例
            item_gap=10,               # 图例项之间间隔10px
            textstyle_opts=opts.TextStyleOpts(font_size=12)  # 图例字体大小
        )
    )

    # 调整绘图区距离上下边界，底部加大留白，给图例腾出空间
    line.options["grid"] = {
        "bottom": "150px",  # 底部留150px，保证图例不会遮挡图表数据
        "top": "60px"       # 顶部留60px，避免标题或其他元素遮挡
    }

    return line
