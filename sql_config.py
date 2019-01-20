# -*- coding: utf-8 -*-

import web

dev_dbw = web.database(dbn='mysql',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='shechipin')

beta_dbw = web.database(dbn='mysql',
    host='127.0.0.1',
    port=3306,
    user='shechipin',
    passwd='Shechipin123',
    db='shechipin')

