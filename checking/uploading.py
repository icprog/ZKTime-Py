#!/usr/bin/python3
# coding=utf-8


"""
考勤数据上传
"""

__author__ = 'LCD'

from cd_tools import *
import json
import requests


def save_date_json(obj):
    d = json.dumps(obj, ensure_ascii=False)
    file = 'Erazar上次读取时间记录.json'
    json_file = open(file, 'w')
    json_file.write(d)
    json_file.close()


def save_log_json(obj):
    d = json.dumps(obj, ensure_ascii=False)
    tim = cd_time_now()
    file = 'tim'+'.json'
    json_file = open(file, 'w')
    json_file.write(d)
    json_file.close()


class Upload(object):

    def __init__(self, log_data, end_time):
        self.post_num = 0
        self.post_num_t = 0
        self.log_data = log_data
        self.end_time = end_time
        self.post_json_to()
        # self.post_json_to_test()

    def post_json_to(self):
        if self.post_num > 10:
            return
        url = 'http://www.xxxxxxxx.net/attends'
        body = {'record': json.dumps(self.log_data)}
        print('-----> 开始上传 : ' + cd_time_now())
        try:
            r = requests.post(url, data=body)
        except:
            print('----->连接失败 ： ' + cd_time_now())
            self.post_num += 1
            self.post_json_to()
        else:
            if r.text == '{"errCode":"0","errMsg":"ok"}':
                print('-----> 上传成功 --> ' + cd_time_now())
                save_date_json(cd_time_to_timestamp(cd_timestamp_to_time(self.end_time, "%Y-%m-%d"), "%Y-%m-%d"))

            else:
                print('----->上传失败 ： ' + cd_time_now())
                print(r)
                self.post_num += 1
                self.post_json_to()

    def post_json_to_test(self):
        if self.post_num_t > 10:
            return
        url = 'http://192.168.1.228:8011/attends'
        body = {'record': json.dumps(self.log_data)}
        print('-----> 上传到228 : ' + cd_time_now())
        try:
            r = requests.post(url, data=body)
        except:
            print('----->连接228失败 ： ' + cd_time_now())
            self.post_num_t += 1
            self.post_json_to_test()
        else:
            if r.text == '{"errCode":"0","errMsg":"ok"}':
                print('-----> 上传228成功 --> ' + cd_time_now())
            else:
                print('----->上传228失败 ： ' + cd_time_now())
                print(r)
                self.post_num_t += 1
                self.post_json_to_test()
