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
            #print name
            rs = self.get_im(name, brand, sex, price, p_pic)
            print len(rs)
            time.sleep(0.02)

        self.__sql_cursor += limit


    def get_im(self, name, brand, sex, price, p_pic):
    	cmd = '''SELECT id, name, brand, sex, price, p_pic 
    	    FROM ImGood 
    	    where brand = "%s" 
    	    and sex = "%s" ''' %(brand, sex)
    	rs = dbw.query(cmd)
    	print cmd
    	return rs


    def get_rows(self, limit_num, number):
	    cmd = "SELECT id, name, brand, sex, price, p_pic \
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