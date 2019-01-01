# -*- coding: utf-8 -*-
import xlrd
import web
import sys
reload(sys)
sys.setdefaultencoding('utf8')


dbw = web.database(dbn='mysql',
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    db='shechipin')


def make_c(row):
    c = []
    n = 0
    for r in row:
        n += 1
        c.append(r)
        print r
    return c

def dump(row):
    c = make_c(row)
    brand = c[0]
    sex = c[1]
    group_name = c[2]
    intra_mirror_id = c[3]
    price = int(c[4])
    size = c[5]
    store = c[6]
    china_yuan = 0
    description = ""
    p_pic = c[7]
    g_pic = c[8]
    prdc, materia, dimension = "","",""

    m = """ insert INTO `ImGood` \
    (name, brand, prdc, sex, materia, dimension, \
    group_name, intra_mirror_id, size, store, \
    price, t_price, china_yuan, description, p_pic, g_pic) \
    values ("%s", "%s", "%s", "%s", "%s", "%s", \
    "%s", "%s", "%s", "%s", \
    %d, %d, %d, "%s", "%s", \
    "%s") """ %(name, brand, prdc, sex, mt, dim, \
    third_party_seq, group_name, intra_mirror_id, size, number, \
    price, t_price, china_yuan, description, p_pic, g_pic)
    print m

    try:
        rows = dbw.query(m)
    except Exception, e:
        print 'str(Exception):\t', str(Exception)
        print 'str(e):\t\t', str(e)
        print 'repr(e):\t', repr(e)
        print 'e.message:\t', e.message
        print 'traceback.print_exc():'; traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()


def process(path_name):
    print "aaa"
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

if  __name__ == "__main__":
    path_name = 'data/im/bally.xlsx'
    process(path_name)

