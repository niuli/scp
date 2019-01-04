#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import system module
import os
import sys
import web
import time
import threading
import datetime
from Queue import *
try:
    import simplejson as json
except ImportError:
    import json

# Import vdc module
#sys.path.append("../vdclib")
#from hs_logger import *
web.config.debug_sql = False


class WorkThread(threading.Thread):
    def __init__(self, no):
        threading.Thread.__init__(self)
        self.input_queue = Queue()
        self.__m_id = no
        self.__m_handle_count = 0
        self.__db = None
        self._stopevent = threading.Event()

    def set_db(self, db):
        self.__db = db

    def set_stop(self):
        self._stopevent.set()

    def join(self, timeout = None):
        """ Stop the thread and wait for it to end. """
        self._stopevent.set( )
        threading.Thread.join(self, timeout)

    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()

    def send(self, item):
        self.input_queue.put(item)

    def run(self):
        try:
            ret = True
            while not self._stopevent.isSet():
                self.__m_handle_count += 1
                item = self.input_queue.get()

                if item is None:
                    #hslogger.get().warninig("none")
                    break

                msg = item
                #hslogger.get().info("r1[%s], r2[%s], r3[%s], r4[%s]" %(r1, r2, r3, r4))

                ret = self.do_work(msg)
                self.input_queue.task_done()
            return ret

        except Exception, e:
            #hslogger.get().warning(""" exception: [%s]  """ %(str(e)))
            return False

    def verify(self, msg):
        return True

    def do_task(self, msg):
        cmd = msg
        rs = self.__db.query(cmd)

    def handle_err_data(self, msg):
        pass

    def do_work(self, msg):
        ret = self.verify(msg)

        if ret == True:
            return self.do_task(msg)
        else:
            self.handle_err_data(msg)
            return False
