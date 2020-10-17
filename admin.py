#!/usr/bin/python
# -*- coding:gbk -*-

import os.path
import sqlite3

database_path = "./library.db"
#CREATE TABLE admin
#                (admin_name TEXT PRIMARY KEY NOT NULL,
#                admin_id         TEXT      NOT NULL,
#                admin_password   TEXT     NOT NULL);

def register_in_admin_file(user_info) :
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "INSERT INTO admin VALUES('%s', '%s', '%s');" \
              % (user_info[0], user_info[1], user_info[2])
    c.execute(string)
    con.commit()
    con.close()
    

#0 无此用户或用户id不对 1 查到该用户,且密码正确 -1 查到该用户，但密码错误
def search_in_admin_file(user_name, user_password = "", user_id = "") :
    con = sqlite3.connect(database_path)
    c = con.cursor()
    string = "SELECT admin_password, admin_id from admin where admin_name = '%s';" \
              % (user_name)
    cursor = c.execute(string)
    r = c.fetchall()
    if len(r) == 0 :
        return 0
    elif user_id != "" :
        if str(r[0][1]) != user_id :
            return 0
        else :
            return 1
    else :
        if str(r[0][0]) == user_password :
            return 1
        else :
            return -1
    con.close()
    

#flag 0 修改密码 1 重置密码
def modify_admin(flag, user_info) :
    con = sqlite3.connect(database_path)
    c = con.cursor()
    if flag == 0 :
        string = "UPDATE admin set admin_password = '%s' where admin_name = '%s';" \
              % (user_info[1], user_info[0])
    elif flag == 1 :
        string = "UPDATE admin set admin_password = '000000' where admin_name = '%s';" \
              % (user_info[0])
    c.execute(string)
    con.commit()
    con.close()
