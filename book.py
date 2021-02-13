#!/usr/bin/python
# -*- coding:gbk -*-

import os.path
import sqlite3

# CREATE TABLE book
#                (book_id TEXT PRIMARY KEY NOT NULL,
#                 book_name TEXT NOT NULL,
#                 book_author TEXT NOT NULL,
#                 book_money REAL NOT NULL,
#                 book_num INT NOT NULL,
#                 book_remain_num INT NOT NULL);

# main 1 2 3 4 7


class Book:
    def __init__(self, con):
        self.con = con

    # book_info = [book_id, book_name, book_author, book_money, book_num, book_remain_num]
    # return 1 ������п�� -1 ���޸� 0 ����鼮
    def add_book(self, book_info):
        ret = 0
        c = self.con.cursor()
        string = "select book_num, book_remain_num from book where book_id = '%s';" % (book_info[0])
        c.execute(string)
        r = c.fetchall()
        if len(r) == 1:
            type_ = str(input("���д���id���Ƿ������Ϣ? y/n\n"))
            if type_ == "y":
                string = "update book set book_name = '%s', book_author = '%s', book_money = %f, \
                            book_num = %d, book_remain_num = %d where book_id = '%s';" \
                         % (book_info[1], book_info[2], book_info[3], book_info[4] + r[0][0],
                            book_info[5] + r[0][1], book_info[0])
                ret = 1
            else:
                ret = -1
        else:
            string = "insert into book values('%s', '%s', '%s', %f, %d, %d);" \
                     % (book_info[0], book_info[1], book_info[2], book_info[3],
                        book_info[4], book_info[5])
        c.execute(string)
        self.con.commit()
        return ret

    # return 0 ɾ���ɹ� -1 ɾ��ʧ�ܣ��޴���
    def delete_book(self, book_info):
        ret = 0
        c = self.con.cursor()
        string = "select book_name from book where book_id = '%s';" % book_info
        c.execute(string)
        r = c.fetchall()
        if len(r) == 0:
            ret = -1
        else:
            string = "delete from book where book_id = '%s';" % book_info
            c.execute(string)
            self.con.commit()
        return ret

    # book_list = [book_name, temp, string, old_string]
    # return 0 �޸ĳɹ� -1 �޸�ʧ�ܣ��޴���
    def modify_book(self, book_list):
        ret = 0
        c = self.con.cursor()
        string = "select %s from book where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
                 % (book_list[1], book_list[0], book_list[0], book_list[0])
        c.execute(string)
        r = c.fetchall()
        if len(r) == 0:
            ret = -1
        else:
            book_list[3] = str(r[0][0])
            string = "update book set %s = '%s' where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
                     % (book_list[1], book_list[2], book_list[0], book_list[0], book_list[0])
            c.execute(string)
            self.con.commit()
        return ret

    # return 0 ��ѯ�ɹ� -1 ��ѯʧ�ܣ��޴���/���鼮���
    # param flag 0 ��ȡ�鼮�б� 1 ��ѯ�鼮
    # book_list = [book_name, "", "", "", "", ""]
    def search_book(self, flag, book_list):
        ret = 0
        c = self.con.cursor()
        if flag == 1:
            string = "select %s from book where book_id = '%s' or book_name = '%s' or book_author = '%s';" \
                     % (book_list[1], book_list[0], book_list[0], book_list[0])
        else:
            string = "select * from book;"
        c.execute(string)
        r = c.fetchall()
        if len(r) == 0:
            ret = -1
        else:
            if flag == 1:
                for i in range(0, 6):
                    book_list[i] = str(r[0][i])
            else:
                for i in range(0, len(r)):
                    book_list.append([r[i][0], r[i][1], r[i][2], r[i][3], r[i][4], r[i][5]])
        return ret

    # param flag > 0 ���+1 < 0 ���-1 ==0 ��治��
    def stock(self, flag):
        pass
