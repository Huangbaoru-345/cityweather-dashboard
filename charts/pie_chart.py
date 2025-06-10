# import pandas as pd
# from pyecharts.charts import Pie
# from pyecharts import options as opts

# def create_pie_chart():
#     df = pd.read_csv('city-weather.csv')

#     # 提取每个城市晴天的天数
#     sunny_counts = df[df['天气'].str.contains('晴')]['城市'].value_counts()

#     data_pair = list(zip(sunny_counts.index.tolist(), sunny_counts.tolist()))

#     pie = Pie(init_opts=opts.InitOpts(width="700px", height="500px"))  # ✅ 更合适的宽高

#     pie.add(
#         series_name="晴天天数占比",
#         data_pair=data_pair,
#         radius=["40%", "70%"],
#         center=["50%", "60%"],  # ✅ 饼图下移居中
#         label_opts=opts.LabelOpts(formatter="{b}: {d}%")
#     )

#     pie.set_global_opts(
#         # title_opts=opts.TitleOpts(title="各城市晴天天数占比"),
#         legend_opts=opts.LegendOpts(
#             orient="horizontal",   # ✅ 横向排列
#             pos_top="5%",          # ✅ 靠上
#             pos_left="center",     # ✅ 水平居中
#             item_gap=20            # ✅ 图例项之间留点间隔
#         )
#     )

#     return pie
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

def create_pie_chart():
    df = pd.read_csv('city-weather.csv')

    # 将“天气”字段中的“转”替换成“/”，然后拆分统计
    df['天气'] = df['天气'].str.replace("转", "/")
    weather_split = df['天气'].str.split('/')
    all_weather = weather_split.explode()  # 把“晴/多云”这种拆开统计

    # 统计所有天气类型出现次数
    weather_counts = all_weather.value_counts()
    data_pair = list(zip(weather_counts.index.tolist(), weather_counts.tolist()))

    # 创建饼图
    pie = Pie(init_opts=opts.InitOpts(width="700px", height="500px"))
    pie.add(
        series_name="天气类型占比",
        data_pair=data_pair,
        radius=["40%", "70%"],
        center=["50%", "60%"],
        label_opts=opts.LabelOpts(formatter="{b}: {d}%")
    )
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="天气类型占比图", pos_top="2%", pos_left="center"),
        legend_opts=opts.LegendOpts(
            orient="horizontal",
            pos_top="bottom",
            pos_left="center"
        )
    )

    return pie  # ✅ 一定不要改成 .render()
