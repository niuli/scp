#!/usr/bin/python
# -*- coding: utf-8 -*-


# Import vdclib module
#from hs_logger import *

# Import my module
from work_thread import WorkThread

class ThreadManager(object):
    def __init__(self):
        self.__m_total_thread_num = 1
        self.__m_work_threads = dict()
        self.__m_sequence_num = 0
        self.__db = None

    def set_thread_num(self, thread_num):
        self.__m_total_thread_num = thread_num

    def set_db(self, db):
        self.__db = db

    def __add_work_thread(self, thread_no, thread):
        self.__m_work_threads[thread_no] = thread

    def round_start(self, number):
        for thread_id in range(number):
            tid = thread_id + 1
            work_thread = WorkThread(tid)
            work_thread.set_db(self.__db)
            work_thread.start()
            self.__add_work_thread(tid, work_thread)


    def round_join(self):
        #hslogger.get().info("self.__m_total_thread_num %d" %(self.__m_total_thread_num))
        for thread_id in range(self.__m_total_thread_num):
            tid = thread_id + 1
            self.__m_work_threads[tid].set_stop()
            self.__m_work_threads[tid].join()


    def do_work(self, msg):
        self.__m_sequence_num += 1
        #hslogger.get().info("do_work %d" %(self.__m_sequence_num))
        work_thread_id = (self.__m_sequence_num % self.__m_total_thread_num) + 1
        self.__m_work_threads[work_thread_id].send(msg)

        return True

