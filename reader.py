#!/usr/bin/python
# -*- coding:gbk -*-

import os.path
import sqlite3

database_path = "./library.db"
#CREATE TABLE reader
#               (reader_id TEXT PRIMARY KEY NOT NULL,
#               reader_name TEXT NOT NULL,
#               reader_address TEXT,
#               reader_phone TEXT);

#main 8 9

#reader_list = [reader_id, reader_name, reader_address, reader_phone, ""]
#0 ��Ӷ��� -1 ���д�id
def add_reader(reader_list) :
    ret = 0
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT reader_name FROM reader where reader_id = '%s';" % (reader_list[0])
    c.execute(string)
    r = c.fetchall()
    if len(r) == 1 :
        print "��id�Ѱ󶨶��ߣ������id��"
        reader_list[1] = r[0][0]
        ret = -1
    else :
        string = "INSERT INTO book VALUES('%s', '%s', '%s', '%s');" \
                 % (reader_list[0], reader_list[1], reader_list[2], reader_list[3])
        c.execute(string)
        con.commit()
    con.close()
    return ret


#reader_list = [reader_id, ""]
#0 ɾ���ɹ� -1 ���޴���
def delete_reader(reader_list) :
    ret = 0
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT reader_name FROM reader where reader_id = '%s';" % (reader_list[0])
    c.execute(string)
    r = c.fetchall()
    if len(r) == 0 :
        print "���޴˶���"
        ret = -1
    else :
        reader_list[1] = r[0][0]
        string = "DELETE FROM reader where reader_id = '%s';" % (reader_lisr[0])
        c.execute(string)
        con.commit()
    con.close()
    return ret


def show_reader_list(reader_list) :
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT * FROM reader;"
    c.execute(string)
    r = c.fetchall()
    for l in r :
        reader_list.append([str(l[0]), str(r[1], str(r[2]), str(r[3])
