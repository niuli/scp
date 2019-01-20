# -*- coding: utf-8 -*-
import xlrd
import web
import sys
reload(sys)
sys.setdefaultencoding('utf8')
web.config.debug_sql = False


from sql_config import *

dbw = dev_dbw


def make_c(row):
    c = []
    n = 0
    for r in row:
        n += 1
        if n == 6:
            continue
        if n == 7:
            continue
        if n == 8:
            continue
        if n == 9:
            continue
        c.append(r)
    return c

def get_price(number):
    price = float(number) * 100
    return int(price)

def dump(row):
    c = make_c(row)
    c[4] = c[4][1:]
    c[5] = c[5][1:]
    c[6] = c[6][1:]

    name = c[0]
    brand = c[1].lower()
    size = c[2]
    store = c[3]
    price = get_price(c[4])
    t_price = int(c[5])
    china_yuan = int(c[6])
    description = c[7]
    p_pic = c[8]
    g_pic = c[9]

    prdc, seq, materia, dimension = get_info(description)
    sex = get_sex(name)
    third_party_seq, group_name, intra_mirror_id = seq, name.replace("男士", "").replace("女士", ""), ""
    #print prdc, seq, materia, dimension

    m = """ insert INTO `DBuy` \
    (name, brand, prdc, sex, materia, dimension, \
    third_party_seq, group_name, intra_mirror_id, size, store, \
    price, t_price, china_yuan, description, p_pic, g_pic) \
    values ("%s", "%s", "%s", "%s", "%s", "%s", \
    "%s", "%s", "%s", "%s", "%s", \
    %d, %d, %d, "%s", "%s", \
    "%s") """ %(name, brand, prdc, sex, materia, dimension, \
    third_party_seq, group_name, intra_mirror_id, size, store, \
    price, t_price, china_yuan, description, p_pic, g_pic)

    try:
        rows = dbw.query(m)
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():'; traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        #print m


def get_info(desc):
    desc = desc.replace("[", "").replace("]", "").replace(" ", "")
    rs = desc.split(',')
    c = 0
    d = dict()
    l1, l2 = [], []
    for r in rs:
        if c%2 == 0:    
            l1.append(r)
        if c%2 == 1:
            l2.append(r)
        c += 1

    prdc, seq, mt, dim = "", "", "", ""
    for i in range(0, len(l1)):
        k = l1[i]
        v = l2[i]
        if k == "产地":
            prdc = v
        if k == "编号":
            seq = v
        if k == "材质":
            mt = v
        if k == "尺寸":
            dim = v
    return prdc, seq, mt, dim

def get_sex(name):
    sex = "unknow"
    if (name.find("女士") != -1):
        sex = "women"
    elif (name.find("男士") != -1):
        sex = "men"
    return sex


def process(path_name):
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
            dump(c)
        except:
            continue

def do_all():

    import os
    path='./data/dbuy'
    for dirpath,dirnames,filenames in os.walk(path):
        for file in filenames:
            fullpath=os.path.join(dirpath,file)
            print fullpath
            process(fullpath)


if  __name__ == "__main__":
    #path_name = 'data/dbuy/BALLY.xlsx'
    path_name = 'data/dbuy/PRADA.xlsx'
    do_all()

    #process(path_name)

