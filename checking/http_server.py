#!/usr/bin/python3
# coding=utf-8


"""
考勤机http访问入口  提供接口服务，可在浏览器访问调起
"""

__author__ = 'LCD'

import sys
from flask import Flask,request
import flask_restful
from zk_read import *
from cd_tools import *
import json


app = Flask(__name__)
api = flask_restful.Api(app)
t = ReadUserData(2)


def read_zk(start, end):
    global t
    if start:
        t.start_time = int(start)
    else:
        t.start_time = cd_timestamp()-2678400

    if end:
        t.end_time = int(end)
    else:
        t.end_time = cd_timestamp()

    make_date_begin_request(t.start_time, t.end_time)
    s = cd_timestamp()
    t.read_user_all()
    t.make_log_data()
    t.prefetch_all_log_data()
    e = cd_timestamp()
    print('用时--->' + str(e - s))
    # t.save_excel_xlsx()
    # t.save_excel_xls()
    # t.post_num = 0
    # t.post_json_to()
    # save_json(t.log_data)
    # save_date_json(cd_time_now('%Y-%m-%d'))


class records(flask_restful.Resource):
    def get(self, attendance):
        params = request.values
        start_time = params.get('start')
        end_time = params.get('end')
        print('---输入------->')
        print(params)
        print(start_time)
        print(end_time)
        print('---------->')
        read_zk(start_time, end_time)
        res = json.dumps(t.log_data, ensure_ascii=False)
        return res


api.add_resource(records, '/<string:attendance>')


if __name__ == '__main__':
    app.run(debug=False, port=8998, host='0.0.0.0')
    # 通过浏览器访问 http://192.168.0.190:8998/attendance?start=1539014492&end=1539143944

