#!/usr/bin/python
# -*- coding: utf-8 -*- 

# Import system module
import os
import logging
import logging.handlers

class hs_logger():
    def __init__(self):
        print("create logger")
        self.logger = None
        self.log_level = logging.DEBUG
        self.log_file = ""
        self.log_name = ""
        self.log_size = 1024 * 1024 * 100   # 100MB

    def start(self):
        #logdir = os.getcwd() + os.sep + "log"
        (logdir,logfilename) = os.path.split(self.log_file)
        print logdir,logfilename

        if not os.path.exists(logdir):
            os.makedirs(logdir)
        filename = self.log_file
        hs_logger = logging.getLogger(self.log_name)

        # Set handler(RotatingFileHandler) & Formatter
        handler = logging.handlers.RotatingFileHandler(
                filename, maxBytes = self.log_size, backupCount = 10000
                )

        # logging.Formatter([fmt[,datefmt]])
        formatter = logging.Formatter('%(levelname)s: %(asctime)s [%(filename)s:%(lineno)d:%(funcName)s:%(threadName)s]: %(message)s', "%m-%d %H:%M:%S:")
        handler.setFormatter(formatter)

        hs_logger.addHandler(handler)

        # Set handler(StreamHandler)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        hs_logger.addHandler(stream_handler)

        # Set log level
        hs_logger.setLevel(self.log_level)

        self.logger = hs_logger

    def get(self):
        return self.logger

