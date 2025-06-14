import requests
from bs4 import BeautifulSoup
import csv
import time
import os

def update_weather_csv():
    city_dict = {
        '广州市': 59287,
        '深圳市': 59493,
        '重庆市': 60025,
        '北京市': 54511,
        '上海市': 58362,
        '杭州市': 58457,
        '武汉市': 57494,
        '南京市': 58238
    }

    output_path = 'city-weather.csv'
    print("📡 正在抓取城市天气数据，请稍候...")

    try:
        with open(output_path, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['日期', '最高温度', '最低温度', '天气', '风向', '城市'])

            for city_name, city_code in city_dict.items():
                print(f"开始爬取：{city_name}")
                seen_dates = set()  #创建一个空集合 seen_dates，用于“去重”，防止写入重复的天气数据

                for month in range(1, 13):
                    url = f'https://tianqi.2345.com/wea_history/{city_code}.htm?&month={month}'
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Safari/537.36'
                    }

                    try:
                        response = requests.get(url, headers=headers, timeout=10)  #请求网页
                        response.encoding = 'utf-8'   #设置网页编码
                        soup = BeautifulSoup(response.text, 'html.parser') #解析html
                        table = soup.find('table', class_='history-table') #找表格，查找网页中 class 是 "history-table" 的 <table> 表格

                        if not table:   #如果 table 是 None，就跳过这个月的数据抓取
                            print(f"[警告] {city_name} {month} 月找不到天气数据表格，跳过")
                            continue

                        rows = table.find_all('tr')[1:]   #提取表格行获取表格中所有行 <tr>，但去掉第一行（通常是表头）

                        if not rows:  
                            print(f"[警告] {city_name} {month} 月无数据，跳过")
                            continue

                        for row in rows: #遍历每一行 每一行 <tr> 包含若干 <td>，即日期、温度、天气等信息
                            cols = row.find_all('td')
                            if len(cols) >= 5:
                                date = cols[0].get_text(strip=True)   # 取出日期（第1列）提取字段 构造一个唯一标识 城市名-日期，用于判断是否重复
                                key = f"{city_name}-{date}"
                                if key in seen_dates:
                                    continue

                                high = cols[1].get_text(strip=True)  #提取其他字段 所有 get_text(strip=True) 会去掉多余空格或换行
                                low = cols[2].get_text(strip=True)
                                weather = cols[3].get_text(strip=True)
                                wind = cols[4].get_text(strip=True)

                                writer.writerow([date, high, low, weather, wind, city_name])  #写入csv
                                seen_dates.add(key) #记录这个日期，防止下次重复写

                        time.sleep(1)  #每次请求后强制等待 1 秒 防止请求太频繁被网站封禁（反爬虫保护）
                    except Exception as e: #如果网页请求失败、解析失败等，都会进入这个 except 块
                        print(f"[错误] 抓取 {city_name} {month} 月失败：{e}")

        print("✅ 所有城市天气数据抓取完毕，保存为 city-weather.csv")
    except Exception as err: #为了防止写入 CSV 文件时发生错误时程序崩溃
        print(f"❌ 写入 CSV 时出错: {err}")
