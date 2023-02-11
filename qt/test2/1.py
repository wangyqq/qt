import flask
from flask import Flask, request, render_template
import requests
from lagouwang import lagouSpitder

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('papa.html')

@app.route('/run_spider', methods=['POST'])
def handle_data():
    name = request.form['spider_name']
    print(1111)
    if name == '拉钩':
        spider = lagouSpitder()
        spider.run()
    return 'Hello ' + name

@app.route('/python接口地址', methods=['POST'])
def get_value():
    value = flask.request.form['value']
    print(value)
    return "OK"



if __name__ == '__main__':
	app.run(host='127.0.1.3',port=5555)


