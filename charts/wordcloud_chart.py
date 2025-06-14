import pandas as pd
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from collections import Counter

def create_weather_wordcloud():
    df = pd.read_csv('city-weather.csv')
    weather_descriptions = df['天气'].dropna().tolist()
    
    all_words = []
    for desc in weather_descriptions:
        for w in desc.replace('转', ' ').replace(',', ' ').split():
            all_words.append(w)
    
    word_counts = Counter(all_words)
    data_pair = list(word_counts.items())

    wordcloud = (
        WordCloud(
            init_opts=opts.InitOpts(
                width="800px",          # 适当增加宽度
                height="600px",         # 适当增加高度
                page_title="天气词云",  # 设置页面标题
                bg_color="transparent",       # 背景色（可选）
                # theme="transparent",          # 主题（可选）
                renderer="canvas",      # 渲染方式（默认canvas，可选svg）
            )
        )
        .add(
            series_name="天气词频",
            data_pair=data_pair,
            word_size_range=[20, 80],
            shape="circle",            # 词云形状（可选：circle, cardioid, diamond, triangle...）
            rotate_step=20,           # 旋转角度间隔（可选）
            textstyle_opts=opts.TextStyleOpts(
            font_family="Microsoft YaHei"
        )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                # title="天气描述词云",
                pos_left="center",     # 标题居中
                pos_top="20",          # 距离顶部20px
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter="{b}: {c}次"  # 悬停提示格式
            ),
        )
    )
    
    return wordcloud