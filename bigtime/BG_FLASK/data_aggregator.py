from datetime import datetime, timedelta
import pytz
from curl_cffi import requests
import csv
from collections import defaultdict


class DataAggregator:
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies
        self.spawn_intervals = {
            ('Rare', 'Small'): 72,
            ('Rare', 'Medium'): 66,
            ('Rare', 'Large'): 60,
            ('Epic', 'Small'): 66,
            ('Epic', 'Medium'): 60,
            ('Epic', 'Large'): 54,
            ('Legendary', 'Small'): 60,
            ('Legendary', 'Medium'): 54,
            ('Legendary', 'Large'): 48,
            ('Mythic', 'Small'): 54,
            ('Mythic', 'Medium'): 48,
            ('Mythic', 'Large'): 42,
            ('Exalted', 'Small'): 48,
            ('Exalted', 'Medium'): 42,
            ('Exalted', 'Large'): 36
        }
        # 提取所需信息
        self.extracted_info = []
        self.aggregated_data = defaultdict(lambda: {'count': 0, 'issuedIds': []})

    def fetch_data(self):
        response = requests.get(self.url, impersonate='chrome110', cookies=self.cookies)
        if response.status_code == 200:
            # 解析返回的JSON数据
            data = response.json()
            for item in data["items"]:
                issued_id = item["issuedId"]
                name = item["metadata"]["name"]
                last_cracked_hour_glass_drop_time = None
                for attribute in item["extra"]["attributes"]:
                    if attribute["name"] == "LastCrackedHourGlassDropTime":
                        last_cracked_hour_glass_drop_time = attribute["value"]
                        break

                self.extracted_info.append({
                    "issuedId": issued_id,
                    "name": name,
                    "LastCrackedHourGlassDropTime": last_cracked_hour_glass_drop_time
                })
            return self.extracted_info

    def process_data(self, data):
        for item in data:
            # 从name属性提取rarity和size
            name_parts = item['name'].split()  # ['Epic', 'Medium', 'SPACE']
            rarity = name_parts[0]  # 'Epic'
            size = name_parts[1]  # 'Medium'
            issued_id = item["issuedId"]

            # 提取和计算下一次生成时间
            next_spawn_str = self.calculate_next_spawn(rarity, size, item)
            if next_spawn_str != "Invalid rarity or size":
                key = (rarity, size, next_spawn_str)
                self.aggregated_data[key]['count'] += 1
                self.aggregated_data[key]['issuedIds'].append(issued_id)

    def calculate_next_spawn(self, rarity, size, item):
        dt_parts = item['LastCrackedHourGlassDropTime'].split('T')
        date_parts = dt_parts[0].split('-')  # ['2024', '03', '04']
        time_parts = dt_parts[1].split(':')  # ['07', '07', '59.545Z']
        year = int(date_parts[0])  # 2024
        month = int(date_parts[1])  # 03
        day = int(date_parts[2])  # 04
        hour = int(time_parts[0])  # 07
        minute = int(time_parts[1])  # 07

        last_drop_time = datetime(year, month, day, hour, minute, tzinfo=pytz.utc)
        interval_hours = self.spawn_intervals.get((rarity, size))
        if interval_hours:
            adjusted_time = last_drop_time + timedelta(hours=interval_hours)
            next_spawn_time = adjusted_time.astimezone(pytz.timezone("Asia/Shanghai")).strftime('%Y-%m-%d %H:%M')
            return next_spawn_time
        else:
            return "Invalid rarity or size"

    def save_to_csv(self, filename):
        sorted_items = sorted(self.aggregated_data.items(), key=lambda x: datetime.strptime(x[0][2], '%Y-%m-%d %H:%M'))
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['稀有度', '大小', '下次掉落时间', '数量', '土地id'])
            for (rarity, size, next_spawn_str), info in sorted_items:
                writer.writerow([rarity, size, next_spawn_str, info['count'], ';'.join(map(str, info['issuedIds']))])

    def run(self):
        data = self.fetch_data()
        if data:
            self.process_data(data)
            self.save_to_csv('combined_data.csv')
            print(f"数据已经保存到CSV文件：combined_data.csv")
            return 1
        print('没有爬取到数据')




if __name__ == '__main__':
    # 使用示例
    url = "https://api.openloot.com/v2/market/items/in-game?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&page=1&pageSize=1000&sort=name%3Aasc&tags=space"

    cookies = {
        'name': 'your_cookie_here'  # 请替换为实际的cookie值
    }

    aggregator = DataAggregator(url, cookies)
    aggregator.run()
