#!/usr/bin/python3
# coding=utf-8


"""
考勤机数据读取
通过 pywin32 链接SDK，使用SDK接口服务
"""

__author__ = 'LCD'

import sys
import win32com.client
from cd_tools import *


key_name = 'name'
key_record = 'record'
# 链接SDK
zk = win32com.client.Dispatch('zkemkeeper.ZKEM.1')
zk_ip = '192.168.1.238'


def user_name_to_gbk(name):
    return str(name.split(u'\x00')[0].encode('gbk'), encoding="gbk")


class Read(object):
    start_time = 0
    end_time = 0

    def __init__(self, start, end):
        self.start_time = 0
        self.end_time = 0
        self.post_dates = []
        self.make_times(start, end)
        self.post_num = 0
        self.post_num_t = 0
        self.user = {}
        self.log_data = None
        s = cd_timestamp()
        self.connect_net()
        e = cd_timestamp()
        self.cost_time = int(e - s)

    def make_times(self, start, end):
        if start:
            self.start_time = int(start)
        else:
            self.start_time = cd_timestamp() - 2678400

        if end:
            self.end_time = int(end)
        else:
            self.end_time = cd_timestamp()

        last = cd_timestamp_to_time(self.start_time, '%Y-%m-%d')
        now = cd_timestamp_to_time(self.end_time, '%Y-%m-%d')
        self.post_dates = cd_make_date_list(last, now, '/')
        self.post_dates.append(cd_join_change(now, '-', '/'))

    def connect_net(self):
        print('-----连接考勤机')
        if not zk.Connect_Net(zk_ip, 4370):
            print('-----连接失败 : ' + cd_time_now())
            # sys.exit(1)
            self.log_data = '考勤机连接失败'
        else:
            self.read_user_all()

    def read_user_all(self):
        print('-----读取所有员工')
        if zk.ReadAllUserID(1):  # read All checkin data
            while 1:
                zk_num, user_id, user_name, pwd, privilege, state = zk.SSR_GetAllUserInfo(1)
                if not zk_num:
                    break
                elif state:
                    self.user[user_id] = user_name_to_gbk(user_name)
            self.make_post_json_all()
        else:
            print('-----读取所有员工信息失败 : ' + cd_time_now())
            self.log_data = '读取员工信息失败'

    def make_post_json_all(self):
        self.log_data = {}
        for item in self.user:
            self.log_data[item] = {}
            for t in self.post_dates:
                self.log_data[item][t] = {key_name: self.user[item],
                                          key_record: []
                                          }
        self.prefetch_all_log_data()

    def prefetch_all_log_data(self):
        print('-----读取考勤记录')
        if zk.ReadAllGLogData(1):  # read All checkin data
            self.read_all_log_data()
        else:
            print('-----读取考勤记录失败 : ' + cd_time_now())
            self.log_data = '读取考勤记录失败'

    def read_all_log_data(self):
        """
        :return: 读取考勤记录之前先记录当前时间节点
        """
        while 1:
            zk_num, user_id, verify, state, yy, month, dd, hh, mm, ss, code = zk.SSR_GetGeneralLogData(1)
            if not zk_num:
                # print('break--1')
                break
            self.data_processing_post_json_all(user_id, yy, month, dd, hh, mm)

    def time_processing(self, s):
        s = str(s)
        if len(s) == 1:
            s = '0' + s
        return s

    def data_processing_post_json_all(self, user_id, yy, month, dd, hh, mm):
        """
        :param user_id:用户ID
        :param yy:
        :param month:
        :param dd:
        :param hh:
        :param mm:
        :return:
        1, 检查当前是否有该用户
        2，检查该用户当前是否已打卡，写入打卡时间，没有则存入first，有则存入last
        获取时间段
        以时间段 和用户 id 建立  json
        """
        month = self.time_processing(month)
        dd = self.time_processing(dd)
        hh = self.time_processing(hh)
        mm = self.time_processing(mm)
        value_date = str(yy) + '/' + month + '/' + dd
        value_time = hh + ':' + mm
        value_timestamp = cd_time_to_timestamp(str(yy)+'-'+month+'-'+dd+' '+hh+':'+mm+':00')
        if (value_timestamp > self.start_time) and (value_timestamp <= self.end_time):
            if user_id in self.log_data:
                if value_date in self.log_data[user_id]:
                    # print('记录---------->')
                    self.log_data[user_id][value_date][key_record].append(value_time)


if __name__ == '__main__':

    Read(1538323200, 1542012760)