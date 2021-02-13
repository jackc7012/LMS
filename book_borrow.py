#!/usr/bin/python
# -*- coding:gbk -*-

import os
import time
import datetime
import sqlite3

database_path = "./library.db"
#CREATE TABLE book_borrow
#                       (reader_id TEXT PRIMARY KEY NOT NULL,
#                       book1 TEXT NOT NULL,
#                       book1_time TEXT NOT NULL,
#                       book2 TEXT,
#                       book2_time TEXT,
#                       book3 TEXT,
#                       book3_time TEXT,
#                       book4 TEXT,
#                       book4_time TEXT,
#                       book5 TEXT,
#                       book5_time TEXT,
#                       book6 TEXT,
#                       book6_time TEXT,
#                       book7 TEXT,
#                       book7_time TEXT,
#                       book8 TEXT,
#                       book8_time TEXT);

#main 5 6

#book_list = [book_id_1, book_id_2, ...]
#return ���������
def borrow_book(reader_id, book_list) :
    ret = 0
    book_borrow_list = []
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT book1, book2, book3, book4, book5, book6, book7, book8 FROM book \
                where reader_id = '%s';" % (reader_id)
    c.execute(string)
    r = c.fetchall()
    if len(r) == 1 :
        pass
    con.close()
    return ret


def book_borrow(reader_id, book_list) :
    book_config = ConfigParser.ConfigParser()
    book_borrow_config = ConfigParser.ConfigParser()
    
    if os.path.exists(book_path) == False :
        open(book_path, "w").close()
    if os.path.exists(book_borrow_path) == False :
        open(book_borrow_path, "w").close()
        
    book_config.read(book_path)
    book_borrow_config.read(book_borrow_path)

    #��ȡ���ڵļ���ǰ��治Ϊ0���鼮id
    book_config_list = book_config.sections()
    book_borrow_list = []
    for l in book_list :
        if l not in book_config_list or book_config.get(l, "book_remain_num") == "0" :
            print("�鼮id %sδ�п��" % (l))
        else :
            book_borrow_list.append(l)

    #������id���鼮id����book_borrow.ini��
    #����д˶��߽����ˣ�������ͼ��
    if book_borrow_config.has_section(reader_id) :
        num = len(book_borrow_config.options(reader_id))
        start_num = num + 1
        book_borrow_list_num = len(book_borrow_list)
        #����8������ֻ�ܽ��8��
        if num + book_borrow_list_num > 8 :
            print("һ������8��,�˴ν���ǰ%d�����Ƚ���" % (8 - num))
            for i in xrange(0, num) :
                book_borrow_list.pop()
                
        for i in xrange(0, len(book_borrow_list)) :
            #���book_borrow.ini
            book_num = "book_" + str(start_num + i)
            time_day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            book = ("book:%s\t\ttime:%s" % (book_borrow_list[i], time_day))
            book_borrow_config.set(reader_id, book_num, book)
            #book.ini�е�ǰ���-1
            book_remain_num = int(book_config.get(book_borrow_list[i], "book_remain_num"))
            book_config.set(book_borrow_list[i], "book_remain_num", str(book_remain_num - 1))
            
    #û�д˶��߽��飬�����Ӵ˶���
    else :
        book_borrow_config.add_section(reader_id)
        for i in xrange(0, len(book_borrow_list)) :
            #���book_borrow.ini
            book_num = "book_" + str(i)
            time_day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            book = ("book:%s\t\ttime:%s" % (book_borrow_list[i], time_day))
            book_borrow_config.set(reader_id, book_num, book)
            #book.ini�е�ǰ���-1
            book_remain_num = int(book_config.get(book_borrow_list[i], "book_remain_num"))
            book_config.set(book_borrow_list[i], "book_remain_num", str(book_remain_num - 1))

    #����ini
    book_config.write(open(book_path, "w"))
    book_borrow_config.write(open(book_borrow_path, "w"))


def book_return(reader_id, book_list) :
    book_config = ConfigParser.ConfigParser()
    book_borrow_config = ConfigParser.ConfigParser()
    
    if os.path.exists(book_path) == False :
        open(book_path, "w").close()
        return -1
    if os.path.exists(book_borrow_path) == False :
        open(book_borrow_path, "w").close()
        return -1
        
    book_config.read(book_path)
    book_borrow_config.read(book_borrow_path)

    #��ȡreader_id��items
    if book_borrow_config.has_section(reader_id) == False :
        return -1.0
    book_borrow_items = book_borrow_config.items(reader_id)
    arrears = 0.0
    for l in book_borrow_items :
        #��ȡ�鼮id�ͽ���ʱ�� book[-1]���鼮id borrow_time[-1]�ǽ���ʱ��
        i = l[1]
        li = i.split("\t\t")
        book = li[0].split(":")
        borrow_time = li[1].split(":")
        if book[-1] in book_list :
            #����book_list�е��鼮�����㷣�ɾ��������Ϣ
            time_day = time.strftime('%Y.%m.%d',time.localtime(time.time()))
            time_day = datetime.datetime.strptime(time_day,"%Y.%m.%d")
            d = datetime.datetime.strptime(borrow_time[-1],"%Y.%m.%d")
            if (time_day - d).days > 30 :
                arrears = arrears + (0.1 * ((time_day - d).days - 30))
            book_borrow_config.remove_option(reader_id, l[0])

            #book.ini�е�ǰ���+1
            book_remain_num = int(book_config.get(book[-1], "book_remain_num"))
            book_config.set(book[-1], "book_remain_num", str(book_remain_num + 1))

    #�����Ӧsection�µ�optionΪ0��ɾ����Ӧ��section
    if len(book_borrow_config.items(reader_id)) == 0 :
        book_borrow_config.remove_section(reader_id)

    #����ini
    book_config.write(open(book_path, "w"))
    book_borrow_config.write(open(book_borrow_path, "w"))
    return arrears
        
