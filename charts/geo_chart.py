from pyecharts.charts import Geo
from pyecharts import options as opts

def geo_chart():
    cities = ['广州市', '深圳市', '重庆市', '北京市', '杭州市', '武汉市', '南京市', '上海市']
    data = [(city, 1) for city in cities]

    geo = (
        Geo()
        .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#87CEFA"))
        .add(
            "爬取城市",
            data,
            type_="scatter",
            color="yellow",
            symbol_size=15,
            label_opts=opts.LabelOpts(is_show=True, formatter="{b}"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="城市分别"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return geo
