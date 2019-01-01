# -*- coding: utf-8 -*-
import xlrd
import web
import sys
reload(sys)
sys.setdefaultencoding('utf8')
web.config.debug_sql = False
import time
import re


dbw = web.database(dbn='mysql',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='shechipin')

mdict = {"手拿包":"clutch-bags"}

def sleep_ex(n):
    assert isinstance(n, (int, basestring)), repr(n)
    if isinstance(n, basestring):
        n, u = re.match(r'^(\d+)([smh])?$', n.lower()).groups()
        n = int(n) * {None: 1, 's': 1, 'm': 60, 'h': 3600}[u]
        time.sleep(n)

class DbuyMerger(object):
    def __init__(self):
        self.__dispatch_interval  = '1s'
        self.__sql_cursor         = 0
        self.__sql_jump           = 500
        self.__sql_handle         = 0
        self.__old_count          = 0
        self.__count              = 0


    def dispatch(self):
        start, limit = self.__sql_cursor, self.__sql_jump
        print(""" scan progress: %d, %d """ %(start, limit))
        rows = self.get_rows(start, limit)
        self.__sql_handle = 0

        for r in rows:
            self.__sql_handle += 1
            self.__count      += 1
            gid     = r['id']
            name     = r['name']
            brand  = r['brand']
            sex = r['sex']
            price = r['price']
            p_pic = r['p_pic']
            group_name = r['group_name']
            if (group_name.find("手拿包") != -1):
                group_name = group_name.replace("手拿包", "clutch-bags")
                rs = self.get_im(name, brand, sex, price, p_pic, group_name)
                ret, min_p, p_pic1 = self.find_best_score(rs, price)
                print ret, min_p, p_pic1, p_pic
            time.sleep(0.02)

        self.__sql_cursor += limit

    def find_best_score(self, rs, price2):
    	ret = 0
    	min_p = 1000
    	for r in rs:
    		price = r['price']
    		gid = r['id']
    		p_pic = r['p_pic']

    		tmp = abs (price2 - price)
    		if tmp < min_p:
    			min_p = tmp
    			ret = gid
        return ret, min_p, p_pic



    def get_im(self, name, brand, sex, price, p_pic, group_name):
        cmd = '''SELECT id, name, brand, sex, price, p_pic 
            FROM ImGood 
            where brand = "%s" 
            and sex = "%s" and
            group_name = "%s" ''' %(brand, sex, group_name)
        rs = dbw.query(cmd)
        return rs


    def get_rows(self, limit_num, number):
        cmd = "SELECT id, name, brand, sex, price, p_pic, group_name \
            FROM DBuy \
            ORDER BY id \
            ASC LIMIT %d, %d" %(limit_num, number)
        rows = dbw.query(cmd)
        return rows

    def do_merge(self):
        while True:
            sleep_ex(self.__dispatch_interval)
            self.dispatch()
            print(""" sql handle : %d, __old_count :%d, count: %d """ %(self.__sql_handle, self.__count, self.__count))

            if self.__sql_handle == 0:
                break
            if self.__count  > self.__old_count:
                self.__old_count = self.__count
                continue


if __name__ == "__main__":
    merger = DbuyMerger()
    merger.do_merge()

	#process()