#!/usr/bin/python
# -*- coding:gbk -*-

import sqlite3

database_path = "./library.db"
# CREATE TABLE admin
#                (admin_id TEXT PRIMARY KEY NOT NULL,
#                 admin_name       TEXT       NOT NULL,
#                 admin_password   TEXT       NOT NULL);


class Admin:
    def __init__(self):
        self.con = sqlite3.connect(database_path)

    def __del__(self):
        self.con.close()

    def get_db_con(self):
        return self.con

    # param user_info = [admin_id, admin_name, admin_password]
    def register_in_admin_db(self, user_info):
        c = self.con.cursor()
        string = "insert into admin values('%s', '%s', '%s');" % (user_info[0], user_info[1], user_info[2])
        c.execute(string)
        self.con.commit()

    # param user_info = [admin_id, admin_password, admin_name]
    # return 0 无此用户 1 查到该用户,且密码正确 -1 查到该用户，但密码错误
    def search_in_admin_db(self, user_info):
        c = self.con.cursor()
        string = "select admin_name, admin_password from admin where admin_id = '%s';" % user_info[0]
        cursor = c.execute(string)
        r = c.fetchall()
        if len(r) == 0:
            return 0
        else:
            if user_info[1] != "":
                if str(r[0][1]) == user_info[1]:
                    user_info.append(r[0][0])
                    return 1
                else:
                    return -1
            else:
                if user_info[2] != r[0][0]:
                    return 0
                else:
                    return 1

    # param flag 0 修改密码 1 重置密码
    def modify_in_admin_db(self, flag, user_info):
        c = self.con.cursor()
        if flag == 0:
            string = "update admin set admin_password = '%s' where admin_id = '%s';" % (user_info[1], user_info[0])
        elif flag == 1:
            string = "update admin set admin_password = '000000' where admin_id = '%s';" % (user_info[0])
        c.execute(string)
        self.con.commit()
