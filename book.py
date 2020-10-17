#!/usr/bin/python
# -*- coding:gbk -*-

import os.path
import sqlite3

database_path = "./library.db"
#CREATE TABLE book
#               (book_id TEXT PRIMARY KEY NOT NULL,
#               book_name TEXT NOT NULL,
#               book_author TEXT NOT NULL,
#               book_money REAL NOT NULL,
#               book_num INT NOT NULL,
#               book_remain_num INT NOT NULL);

#main 1 2 3 4 7

#book_info = [book_id, book_name, book_author, book_money, book_num, book_remain_num]
#1 添加已有库存 -1 不修改 0 添加书籍
def add_book(book_info) :
    ret = 0
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT book_num, book_remain_num FROM book where book_id = '%s';" % (book_list[0])
    c.execute(string)
    r = c.fetchall()
    if len(r) == 1 :
        type_ = str(raw_input("已有此书id，是否更新信息? y/n\n"))
        if type_ == "y" :
            string = "UPDATE book set book_name = '%s', book_author = '%s', book_money = %f, \
                        book_num = %d, book_remain_num = %d where book_id = '%s';" \
                         % (book_list[1], book_list[2], book_list[3], book_list[4] + r[0][0], \
                            book_list[5] + r[0][1], book_list[0])
            ret = 1
        else :
            ret = -1
    else :
        string = "INSERT INTO book VALUES('%s', '%s', '%s', %f, %d, %d);" \
                 % (book_list[0], book_list[1], book_list[2], book_list[3], \
                    book_list[4], book_list[5])
    c.execute(string)
    con.commit()
    con.close()
    return ret


#0 删除成功 -1 删除失败，无此书
def delete_book(book_info) :
    ret = 0
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT * FROM book where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
            % (book_info, book_info, book_info)
    c.execute(string)
    r = c.fetchall()
    if len(r) == 0 :
        ret = -1
    else :
        string = "DELETE FROM book where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
            % (book_info, book_info, book_info)
        c.execute(string)
        con.commit()
    con.close()
    return ret


#0 修改成功 -1 修改失败，无此书
#book_list = [book_name, temp, string, old_string]
def modify_book(book_list) :
    ret = 0
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT %s FROM book where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
            % (book_list[1], book_list[0], book_list[0], book_list[0])
    c.execute(string)
    r = c.fetchall()
    if len(r) == 0 :
        ret = -1
    else :
        book_list[3] = str(r[0][0])
        string = "UPDATE book set %s = '%s' where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
                 % (book_list[1], book_list[2], book_list[0], book_list[0], book_list[0])
        c.execute(string)
        con.commit()
    con.close()
    return ret


#0 查询成功 -1 查询失败，无此书/无书籍库存
#flag 0 获取书籍列表 1 查询书籍
#book_list = [book_name, "", "", "", "", ""]
def search_book(flag, book_list) :
    ret = 0
    con = sqlite3.connect(database_path)
    c = con.cursor()
    if flag == 1 :
        string = "SELECT %s FROM book where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
                % (book_list[1], book_list[0], book_list[0], book_list[0])
    else :
        string = "SELECT %s FROM book;" 
    c.execute(string)
    r = c.fetchall()
    if len(r) == 0 :
        ret = -1
    else :
        if flag == 1 :
            for i in xrange(0, 6) :
                book_list[i] = str(r[0][i])
        else :
            for i in xrange(0, len(r)) :
                book_list.append(r[i][0], r[i][1], r[i][2], r[i][3], r[i][4], r[i][5])
    con.close()
    return ret


#flag >0 库存+1 <0 库存-1 ==0 库存不变
def stock(flag) :
    pass
