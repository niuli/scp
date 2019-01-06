# -*- coding: utf-8 -*-
import xlrd
import web
import sys
import utils
from thread_manager import *
import time

reload(sys)
sys.setdefaultencoding('utf8')
web.config.debug_sql = False

from hs_logger import *

dbw = web.database(dbn='mysql',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='shechipin')


class Dispatcher(object):
    def __init__(self):
        self.__thread_manager     = None
        self.__work_thread_number = 10
        self.__db = dbw


    def do_run(self):
        thread_manager = ThreadManager()
        thread_manager.set_thread_num(self.__work_thread_number)
        thread_manager.set_db(self.__db)

        thread_manager.round_start(self.__work_thread_number)
        self.__thread_manager = thread_manager

        time.sleep(0.5)
        #self.do_check()
    def get_price(self, number):
        price = float(number) * 100
        return int(price)

    def make_sql(self, row):
        c = utils.make_column(row)
        brand = c[0].lower()
        sex = c[1].lower()
        group_name = c[2].lower()
        intra_mirror_id = c[3]
        price = self.get_price(c[4])
        size = c[5]
        store = str(c[6])

        p_pic = c[7]
        g_pic = c[8]
        p_pic = p_pic.replace('"', '')
        g_pic = g_pic.replace('"', '')

        prdc, materia = "",""
        name, dimension = "", ""
        china_yuan, t_price = 0, 0
        description = ""
        #print brand, group_name, intra_mirror_id
        #print price, size, store, sex
        #print p_pic, g_pic

        cmd = """ insert INTO `ImGood` \
        (name, brand, prdc, sex, materia, dimension, \
        group_name, intra_mirror_id, size, store, \
        price, t_price, china_yuan, description, p_pic, g_pic) \
        values ("%s", "%s", "%s", "%s", "%s", "%s", \
        "%s", "%s", "%s", "%s", \
        %d, %d, %d, "%s", "%s", \
        "%s") """ %(name, brand, prdc, sex, materia, dimension, \
        group_name, intra_mirror_id, size, store, \
        price, t_price, china_yuan, description, p_pic, g_pic)
        #self.do_sql(cmd)
        return cmd


    def do_sql(self, cmd):
        try:
            rows = dbw.query(cmd)
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'; traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()


    def process(self, path_name, is_thread):
        data = xlrd.open_workbook(path_name)
        table = data.sheets()[0]

        nrows=table.nrows
        ncols=table.ncols

        for i in range(nrows):
            c = []
            for j in range(ncols):
                row_content = table.col(j)[i].value #先行后列
                col_content = table.row(i)[j].value #先列后行
                content = table.cell(i,j).value
                c.append(content)
            try:
                msg = self.make_sql(c)
                if (is_thread == True):
                    self.__thread_manager.do_work(msg)
                else:
                    self.do_sql(msg)
            except Exception, e:
                print e
                continue


def do_all_path():
    init_log()
    import os
    path='./data/im'
    iMDispatcher = Dispatcher()

    for dirpath,dirnames,filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath,file)
            print fullpath
            iMDispatcher.process(fullpath, False)


def do_one_file():
    init_log()
    path_name = 'data/im/Prada.xlsx'
    #path_name = 'data/im/bally.xlsx'
    hslogger.get().info("iMDispatcher one file" ) 

    iMDispatcher = Dispatcher()
    iMDispatcher.do_run()
    iMDispatcher.process(path_name, True)


def init_log():
    import logging
    hslogger.log_leval = logging.INFO
    hslogger.log_name = "make_sql.log"
    hslogger.log_file = "../log/make_sql.log"
    hslogger.start()

if  __name__ == "__main__":
    do_all_path()

