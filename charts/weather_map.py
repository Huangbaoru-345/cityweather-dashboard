import pandas as pd
from pyecharts.charts import Geo
from pyecharts import options as opts

def create_weather_map():
    cities = ['广州市', '深圳市', '重庆市', '北京市', '杭州市', '武汉市', '南京市', '上海市']
    data = [(city, 1) for city in cities]  # 值设为 1，用于定位

    geo = (
        Geo()
        .add_schema(
            maptype="china",
            itemstyle_opts=opts.ItemStyleOpts(color="#f0f8ff", border_color="#111"),
        )
        .add(
            series_name="爬取城市",
            data_pair=data,
            type_="scatter",
            symbol_size=12,
            label_opts=opts.LabelOpts(is_show=True, formatter="{b}"),
            itemstyle_opts=opts.ItemStyleOpts(color="orange"),
        )
        .set_global_opts(
            # title_opts=opts.TitleOpts(title="已爬取城市分布图"),
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}")
        )
    )
    return geo
