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

#mdict = {"手拿包":"clutch-bags"}

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
        self.__sql_jump           = 100
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
            #print brand, sex, price, group_name
            #if (group_name.find("手拿包") != -1):
            group_name = self.get_group_name(group_name)
            rs = self.get_im(name, brand, sex, price, p_pic, group_name)
            if len(rs) == 0:
                continue
            gid2, min_p, p_pic1 = self.find_best_score(rs, price)
            #print 
            p1, p2 = "", ""
            if p_pic1.find("http") != -1 and p_pic.find("http") != -1:
                p1 = p_pic1.split(",")[0].replace("[", "")
                p2 = p_pic.split(",")[0].replace("[", "")
            #print ret, min_p, p_pic1, p_pic
                print min_p, p1, p2, gid, gid2

            time.sleep(0.01)

        self.__sql_cursor += limit

    # 这里可以优化一下性能，先查找再替换，或者做个前缀索引，KMP之类的
    def get_group_name(self, group_name):
        group_name = group_name.replace("手拿包", "clutch-bags")
        group_name = group_name.replace("及踝靴", "boots/hi-tops")
        group_name = group_name.replace("手提包", "purses")
        group_name = group_name.replace("调节帽", "hats")
        group_name = group_name.replace("长款钱夹", "wallets")
        group_name = group_name.replace("腰带", "blets")
        group_name = group_name.replace("高跟鞋", "highheels")
        group_name = group_name.replace("商务休闲鞋", "business casual shoes")
        group_name = group_name.replace("拖鞋", "sandals/flip flops")
        group_name = group_name.replace("围巾", "scarves")
        group_name = group_name.replace("斜挎包", "shoulder/crossbody bags")
        group_name = group_name.replace("休闲运动鞋", "business casual shoes")
        group_name = group_name.replace("普拉达", "")
        group_name = group_name.replace(" ","")
        return group_name
        #print group_name


    def find_best_score(self, rs, price2):
        ret = 0
        min_p = 1000
        pic =""
        gid = ""
        if len(rs) == 0:
            print "empty line"
            return ret, min_p, p_pic
        for r in rs:
            price = r['price']

            #print "min_p", min_p
            tmp = abs (price2 - price)
            if tmp < min_p:
                min_p = tmp
                gid = r['id']
                p_pic = r['p_pic']
                print price2, price, min_p
        return gid, min_p, p_pic



    def get_im(self, name, brand, sex, price, p_pic, group_name):
        cmd = '''SELECT id, name, brand, sex, price, p_pic 
            FROM ImGood 
            where brand = "%s" 
            and sex = "%s" and
            group_name = "%s" ''' %(brand, sex, group_name)
        rs = dbw.query(cmd)
        #print cmd
        #print len(rs)
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