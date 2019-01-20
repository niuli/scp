#!/usr/bin/python
# -*- coding: utf-8 -*- 

import web
import sys

reload(sys)
sys.setdefaultencoding('utf8')
web.config.debug_sql = False

from sql_config import *

dbw = dew_dbw 

bags = ["购物包","邮差包","手提包","单肩包", "双肩包", "手拿包", "零钱包","斜挎包", "卡包","钥匙包", "单肩背包", "链条手包", 
        "水桶包","相机包","手机包", "迷你背包","拉链钱包","小号肩背包","迷你背包","两用包", "长款钱包",
        "钱包", "链条包", "收纳包", "机车背包", "化妆包", "手拎包", "背包"]

boots = ["运动袜靴", "及踝袜靴", "及踝靴","雪地靴", "短筒靴", "中筒靴", "及膝靴", "过膝靴", "马丁靴"]

#if __name__ == "__main__":
def get_name():    
    cmd = "select distinct group_name from dbuy"
    rs = dbw.query(cmd)
    for r in rs:
        a = r["group_name"]
        if a.find("包") != -1:
            tag = 0
            for l in bags:
                if a.find(l) != -1:
                    tag = 1
                    #print a, "\t", l
            if tag == 0:
                #print a, 0
                continue
        elif a.find("靴") != -1:
            if a.find("包") != -1:
                tag = 0
                for l in bags:
                    if a.find(l) != -1:
                        tag = 1
                    #print a, "\t", l
                if tag == 0:
                    print a, 0
                    #continue
                #print a

        elif a.find("鞋") != -1:
            print a

if __name__ == "__main__":
    #cmd = "select distinct group_name from imgood"
    cmd = "select distinct group_name from Dbuy"
    rs = dbw.query(cmd)
    for r in rs:
        print r["group_name"]


