from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
from datetime import datetime, timedelta
import os
from data_aggregator import DataAggregator
from send_message import CompletionTimeNotifier

app = Flask(__name__)
# 创建并启动你的线程类实例
send_key = "自己的key"
filename = "completion_times.txt"
csv_filename = 'combined_data.csv'  # 替换为你的CSV文件名
notifier = CompletionTimeNotifier(send_key, filename, csv_filename)
notifier.start()


def calculate_completion_time(days, hours, minutes):
    current_time = datetime.now()
    completion_time = current_time + timedelta(days=days, hours=hours, minutes=minutes)
    return completion_time.strftime('%Y-%m-%d %H:%M:%S')


def read_existing_records(filename):
    records = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='ISO-8859-1') as file:
            lines = file.readlines()[1:]  # Skip the header line
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 4:
                    item_name = parts[0]
                    completion_time_str = ' '.join(parts[1:3])
                    count = int(parts[-1])
                    records[item_name] = [datetime.strptime(completion_time_str, '%Y-%m-%d %H:%M:%S'), count]
    return records


def update_records(filename, items_dict):
    sorted_records = sorted(items_dict.items(), key=lambda x: x[1][0])

    with open(filename, 'w') as file:
        file.write(f"物品完成时间：\n")
        file.write(f"{'物品名称':<20}{'完成时间':<19}{'次数'}\n")
        for item_name, (completion_time, count) in sorted_records:
            file.write(f"{item_name:<20}{completion_time.strftime('%Y-%m-%d %H:%M:%S'):<25}{count}\n")

def read_cookie_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            cookie = file.read().strip()
        return cookie
    except FileNotFoundError:
        return None

def save_cookie_to_file(cookie, filepath):
    with open(filepath, 'w') as file:
        file.write(cookie)

# 更新 cookie
@app.route('/shattered-time', methods=['POST'])
def update_cookie():
    data = request.json
    cookie = data.get('cookie')
    if cookie:
        # 保存 cookie 到文件
        save_cookie_to_file(cookie, 'cookie_file.txt')
        return jsonify({'status': 'success', 'message': 'Cookie 更新成功'})
    else:
        return jsonify({'status': 'error', 'message': '未提供 cookie'})

# 运行程序
@app.route('/run-shattered-time', methods=['POST'])
def run_shattered_time():
    cookie = read_cookie_from_file('cookie_file.txt')
    if cookie:
        # 运行 DataAggregator，使用读取的 cookie
        url = "https://api.openloot.com/v2/market/items/in-game?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&page=1&pageSize=1000&sort=name%3Aasc&tags=space"

        aggregator = DataAggregator(url, {'cookie_name': cookie})  # 替换 'cookie_name' 为实际的 cookie 名称
        try:
            aggregator.run()
            file_path = 'combined_data.csv'
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    file_content = file.read()
                return jsonify({'status': 'success', 'message': '操作成功', 'data': file_content})
            else:
                return jsonify({'status': 'error', 'message': '文件不存在'})
        except Exception as e:
            # 如果运行失败，返回异常的详细信息
            return jsonify({'status': 'error', 'message': f'运行失败，错误详情：{str(e)}'}), 500

    else:
        return jsonify({'status': 'error', 'message': 'Cookie 不存在，请先设置 cookie'})


@app.route('/delete/<item_name>')
def delete_item(item_name):
    existing_records = read_existing_records(filename)
    if item_name in existing_records:
        del existing_records[item_name]  # 删除指定的物品
        update_records(filename, existing_records)  # 更新文件
    return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        item_name = request.form['item_name']
        days = int(request.form['days'])
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        completion_time_str = calculate_completion_time(days, hours, minutes)

        existing_records = read_existing_records(filename)
        # 更新或添加记录，包括次数处理
        if item_name in existing_records:
            # 如果物品已存在，更新完成时间并增加次数
            _, count = existing_records[item_name]
            existing_records[item_name] = [datetime.strptime(completion_time_str, '%Y-%m-%d %H:%M:%S'), count + 1]
        else:
            # 如果是新物品，添加记录并设置次数为1
            existing_records[item_name] = [datetime.strptime(completion_time_str, '%Y-%m-%d %H:%M:%S'), 1]
        update_records(filename, existing_records)

    # 读取现有记录，无论是GET还是POST请求
    existing_records = read_existing_records(filename)
    # 转换记录格式以适应模板期望的结构
    records_for_template = {k: [v[0].strftime('%Y-%m-%d %H:%M:%S'), v[1]] for k, v in existing_records.items()}
    return render_template('bigtime.html', records=records_for_template)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
