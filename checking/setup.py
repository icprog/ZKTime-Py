#!/usr/bin/python3
# coding=utf-8


"""
考勤机脚本入口，定时任务
"""

__author__ = 'LCD'


from attendance_read import Read
from uploading import Upload
from cd_tools import *
import schedule
import json


def open_json_file():
    # print('open_json_file')
    try:
        json_file = open("Erazar上次读取时间记录.json", 'r')
    except:
        return cd_time_to_timestamp(cd_make_date_for_now(-32), '%Y-%m-%d')
    else:
        return read_json(json_file)


def read_json(json_file):
    try:
        dic = json.load(json_file)
    except:
        return cd_time_to_timestamp(cd_make_date_for_now(-32), '%Y-%m-%d')
    else:
        return dic


def save_date_json(obj):
    d = json.dumps(obj, ensure_ascii=False)
    file = 'Erazar上次读取时间记录.json'
    json_file = open(file, 'w')
    json_file.write(d)
    json_file.close()


def save_log_json(obj):
    d = json.dumps(obj, ensure_ascii=False)
    tim = cd_time_now('%Y-%m-%d')
    file = tim + '.json'
    json_file = open(file, 'w')
    json_file.write(d)
    json_file.close()


class ReadRecord:
    def __init__(self):
        self.num = 0
        self.read()

    def read(self):
        if self.num >= 10:
            print('------> 错误！没有读到考勤数据')
            print(cd_time_now())
            print('------>')
            return
        start_time = open_json_file()
        end_time = cd_timestamp()

        print('-----> 开始读取记录 从' + cd_timestamp_to_time(start_time))
        t = Read(start_time, end_time)
        if t.log_data:
            if isinstance(t.log_data, str):
                self.num += 1
                self.read()
            elif isinstance(t.log_data, dict):
                print('-----> 读取成功')
                # print(t.log_data)
                save_log_json(t.log_data)
                Upload(t.log_data, t.end_time)
        else:
            self.num += 1
            self.read()


def read_zk():
    ReadRecord()

# 定时任务
read_zk()
schedule.every().day.at("00:00").do(read_zk)
schedule.every().day.at("10:00").do(read_zk)
schedule.every().day.at("14:00").do(read_zk)
schedule.every().day.at("19:00").do(read_zk)

while True:
    schedule.run_pending()


"""
# web 服务
import sys
from flask import Flask, request, jsonify
import flask_restful
from attendance_read import Read


app = Flask(__name__)
api = flask_restful.Api(app)


class records(flask_restful.Resource):
    def post(self, attendance):
        params = request.values
        start_time = params.get('start')
        end_time = params.get('end')
        t = Read(start_time, end_time)
        res = {'data': '', 'msg': '', 'code': 0, 'time': t.cost_time}
        if t.log_data:
            if isinstance(t.log_data, str):
                res['msg'] = t.log_data
            elif isinstance(t.log_data, dict):
                res['code'] = 1
                res['data'] = t.log_data
        else:
            res['msg'] = '未知错误'

        # res = json.dumps(t.log_data, ensure_ascii=False)

        return jsonify(res)

    def get(self, attendance):
        params = request.values
        start_time = params.get('start')
        end_time = params.get('end')
        t = Read(start_time, end_time)
        res = {'data': '', 'msg': '', 'code': 0, 'time': t.cost_time}
        if t.log_data:
            if isinstance(t.log_data, str):
                res['msg'] = t.log_data
            elif isinstance(t.log_data, dict):
                res['code'] = 1
                res['data'] = t.log_data
        else:
            res['msg'] = '未知错误'
        return jsonify(res)


api.add_resource(records, '/<string:attendance>')
app.run(debug=False, port=8998, host='0.0.0.0')
"""

'''
if __name__ == '__main__':
    app.run(debug=False, port=8998, host='0.0.0.0')
'''

