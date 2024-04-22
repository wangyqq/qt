import json
import os
import csv
import requests
import threading
import time
from datetime import datetime, timedelta

class CompletionTimeNotifier(threading.Thread):
    def __init__(self, send_key, filename, csv_filename, notified_items_filename='notified_items.json', check_interval=60):
        super().__init__()
        self.send_key = send_key
        self.filename = filename
        self.csv_filename = csv_filename
        self.notified_items_filename = notified_items_filename
        self.notified_items = self.load_notified_items()
        self.check_interval = check_interval
        self.daemon = True  # 设置为守护线程，确保主程序退出时，线程也会退出

    def load_notified_items(self):
        if os.path.exists(self.notified_items_filename):
            with open(self.notified_items_filename, 'r') as file:
                return json.load(file)
        return {}

    def save_notified_items(self):
        with open(self.notified_items_filename, 'w') as file:
            json.dump(self.notified_items, file)

    def send_wechat_message(self, title, message):
        url = f"https://sctapi.ftqq.com/{self.send_key}.send"
        data = {"text": title, "desp": message}
        requests.post(url, data=data, verify=False)

    def read_completion_times(self):
        completion_times = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='ISO-8859-1') as file:
                lines = file.readlines()[2:]  # Skip the header lines
                for line in lines:
                    parts = line.strip().split(maxsplit=3)
                    if len(parts) == 4:
                        item_name, date_str, time_str, count_str = parts
                        completion_time_str = f"{date_str} {time_str}"
                        try:
                            completion_time = datetime.strptime(completion_time_str, '%Y-%m-%d %H:%M:%S')
                            completion_times.append((item_name, completion_time))
                        except ValueError as e:
                            print(f"Error parsing completion time: {e}")

        if os.path.exists(self.csv_filename):
            with open(self.csv_filename, newline='', encoding='ISO-8859-1') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip the header
                for row in csvreader:
                    rarity, size, drop_time_str = row[:3]  # 根据实际CSV结构调整
                    item_name = rarity + size
                    try:
                        try:
                            # 尝试包含秒的格式
                            drop_time = datetime.strptime(drop_time_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            # 如果失败，则尝试不包含秒的格式
                            try:
                                drop_time = datetime.strptime(drop_time_str, '%Y-%m-%d %H:%M')
                            except ValueError as e:
                                print(f"Error parsing drop time with both formats: {e}")
                                continue
                        completion_times.append((item_name, drop_time))
                    except ValueError as e:
                        print(f"Error parsing drop time: {e}")

        return completion_times

    def format_time_for_notification(self, dt):
        """统一时间格式化为不包含秒的字符串形式"""
        return dt.strftime('%Y-%m-%d %H:%M')

    def check_and_notify(self):
        notified_items = self.load_notified_items()
        completion_times = self.read_completion_times()
        now = datetime.now()
        notice_period = timedelta(minutes=30)
        flexibility = timedelta(minutes=10)

        upcoming_items = []
        for item in completion_times:
            item_id, completion_time = item
            completion_time_str = self.format_time_for_notification(completion_time)
            if item_id in notified_items and completion_time_str == notified_items[item_id]:
                continue
            if -flexibility <= (completion_time - now) <= notice_period + flexibility:
                upcoming_items.append(item)
        for item in upcoming_items:
            try:
                self.send_wechat_message('BIGTIME物品完成提醒', f'{item[0]}将在{self.format_time_for_notification(item[1])}完成')
                self.notified_items[item[0]] = self.format_time_for_notification(item[1])
                self.save_notified_items()
            except Exception as e:
                print(f"Failed to send message for {item[0]}: {e}")

    def run(self):
        while True:
            self.check_and_notify()
            time.sleep(self.check_interval)

# 使用示例
if __name__ == '__main__':
    send_key = ''
    filename = 'completion_times.txt'
    csv_filename = 'combined_data.csv'  # 替换为你的CSV文件名
    notifier = CompletionTimeNotifier(send_key, filename, csv_filename)
    notifier.run()
