import pandas as pd
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from collections import Counter

def create_weather_wordcloud():
    df = pd.read_csv('city-weather.csv')
    # 提取所有天气描述，可能是复合词，拆分后统计词频
    weather_descriptions = df['天气'].dropna().tolist()
    
    # 简单拆分（如果“多云转晴”这种复杂词，可改为更复杂的拆词逻辑）
    all_words = []
    for desc in weather_descriptions:
        # 按空格、逗号、转等拆分
        for w in desc.replace('转', ' ').replace(',', ' ').split():
            all_words.append(w)
    
    word_counts = Counter(all_words)
    data_pair = list(word_counts.items())

    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="600px", height="400px"))
        .add(series_name="天气词频", data_pair=data_pair, word_size_range=[20, 80])
        # .set_global_opts(title_opts=opts.TitleOpts(title="天气描述词云"))
    )
    return wordcloud
