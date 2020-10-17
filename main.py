#!/usr/bin/python
# -*- coding:gbk -*-

import os
import book as b
import admin as a
import reader as r
import book_borrow as bb

now_user = ""
system_version = "1.0.0.0-20200518"
flag = False

#管理员注册
def register() :
    while 1 :
        user_name = raw_input("请输入用户名:")
        flag = a.search_in_admin_file(user_name)
        if flag == 0 :
            break
        else :
            print "此用户名已存在，请更换!!!"
    user_id = raw_input("请输入用户id:")      
    while 1 :
        user_password = raw_input("请输入密码:")
        user_password_again = raw_input("请再次输入密码:")
        if user_password == user_password_again :
            a.register_in_admin_file([user_name, user_id, user_password])
            break
        else :
            print "两次密码输入不一致，请重新输入!!!"
            continue
    print "注册成功"
    raw_input("请按回车键继续")
    os.system("cls")
    

#管理员登录
def login() :
    global now_user
    user_name = raw_input("请输入用户名:")
    while 1 :
        user_password = raw_input("请输入密码:")
        flag = a.search_in_admin_file(user_name, user_password)
        if flag == 1 :
            now_user = user_name
            operater_system()
            break
        elif flag == -1 :
            print "密码错误，请重新输入!!!"
            continue
        elif flag == 0 :
            print "查无此用户!!!"
            break


#版本查询
def get_version() :
    print "sys:%s" % (system_version)
    raw_input("请按回车键继续")


#修改管理员密码
def modify_admin_password() :
    global now_user
    global flag
    user_name = str(raw_input("请输入用户名："))
    if a.search_in_admin_file(user_name) == 0 :
        print "查无此用户!!!"
        return 
    user_password = str(raw_input("请输入当前密码(如为空，将重置密码)："))
    if user_password != "" :
        while 1 :
            user_new_password = str(raw_input("请输入新密码："))
            if user_password == user_new_password :
                print "新老密码不能相同!!!"
                continue
            user_new_password_again = str(raw_input("请重新输入新密码："))
            if user_new_password == user_new_password_again :
                a.modify_admin(0, [user_name, user_new_password])
                print "%s密码修改成功" % (user_name)
                break
            else :
                print "两次密码不一致，请重新输入!!!"
    else :
        user_id_ = str(raw_input("请输入用户id："))
        if a.search_in_admin_file(user_name, user_id = user_id_) == 0:
            print "用户id输入错误!!!"
        else :
            a.modify_admin(1, [user_name])
            print "%s密码重置成功" % (user_name)

    if user_name == now_user :
        now_user = ""
        print "当前用户密码已改变，请重新登录!!!"
        flag = True
        raw_input("请按回车键继续")
    else :
        raw_input("请按回车键继续")
		

#1
def add_book() :
    book_id = str(raw_input("请输入书籍id："))
    book_name = str(raw_input("请输入书名："))  
    book_author = str(raw_input("请输入作者："))   
    book_money = float(raw_input("请输入书本价钱："))
    book_num = int(raw_input("请输入书本的数量："))
    book_remain_num = book_num
    book_info = [book_id, book_name, book_author, book_money, book_num, book_remain_num]
    flag = b.add_book(book_info)
    if flag == 0 :
        print "书本%s添加成功, 图书作者:%s, 图书id:%s, 图书价钱:%s, 图书数量:%s" \
              % (book_name, book_author, book_id, book_money, book_num)
    elif flag == 1 :
        print "书本%s库存成功, 图书作者:%s, 图书id:%s, 图书价钱:%s, 图书数量:%s" \
              % (book_name, book_author, book_id, book_money, book_num)
    else :
        print "添加失败!!!"
    raw_input("请按回车键继续")


#2
def delete_book() :
    get_booklist()
    print "----------------------------"
    book_name = str(raw_input("请输入要查询书籍id/名称/作者:"))
    if b.delete_book(book_name) == 0 :
        print "书本%s删除成功" % (book_name)
    else :
        print "未在库存中找到此书!!!"
    raw_input("请按回车键继续")


#3
def modify_book() :
    get_booklist()
    print "----------------------------"
    book_name = str(raw_input("请输入要查询书籍id/名称/作者:"))
    type_num = int(raw_input("请输入需要修改的内容，1.书名 2.作者 3.价钱 4.书本数量 5.书本剩余数量\n"))
    string = str(raw_input("请输入修改值"))
    old_string = ""
    temp = ""
    if type_num == 1 :
        temp = "book_name"
    elif type_num == 2 :
        temp = "book_author"
    elif type_num == 3 :
        temp = "book_money"
    elif type_num == 4 :
        temp = "book_num"
    elif type_num == 5 :
        temp = "book_remain_num"
    if b.modify_book([book_name, temp, string, old_string]) == 0 :
        print "修改%s属性%s %s->%s 成功" % (book_id, temp, old_string, string)
    else :
        print "未在库存中找到此书!!!"
    raw_input("请按回车键继续")


#4
def search_book() :
    print "----------------------------"
    book_name = str(raw_input("请输入要查询书籍id/名称/作者:"))
    book_list = [book_name, "", "", "", "", ""]
    if b.search_book(1, book_list) == 0 :
        print "书本id:%s, 书名:%s, 作者:%s, 价钱:%s, 书本数量:%s, 书本剩余数量%s.\n" \
              % (book_list[0], book_list[1], book_list[2], book_list[3], book_list[4], book_list[5])
    else :
        print "未在库存中找到此书!!!"
    raw_input("请按回车键继续")


#5
def borrow_book() :
    #读者id
    while 1 :
        reader_id = str(raw_input("请输入读者id:"))
        reader_list = []
        r.show_reader_list(reader_list)
        if reader_id in reader_list[0] :
            break
        else :
            temp = str(raw_input("未查到此读者id!!!\n按0重新输入，按其他退出操作:"))
            if temp == "0" :
                continue
            else :
                return
    #借阅书籍
    book_list = []
    print "请输入书籍id，按0结束:\n"
    while 1 :
        book_id = str(raw_input())
        if book_id == "0" :
            break
        book_list.append(book_id)
        if len(book_list) >= 8 :
            print "借书超过8本,前8本优先借出!!!"
            break
    #查询书籍是否存在及库存
    book_temp = []
    b.search_book(0, book_temp)
    for i in xrange(0, len(book_list)) :
        if book_list[i] not in book_temp[0] :
            book_list.pop(i)
    for i in xrange(0, len(book_list)) :
        for l in book_temp :
            if book_list[i] == l[0] and l[5] == 0 :
                book_list.pop(i)
                break
    bb.book_borrow(reader_id, book_list)
    print "借书成功"
    raw_input("请按回车键继续")
    

#6
def return_book() :
    while 1 :
        reader_id = str(raw_input("请输入读者id:"))
        reader_list = r.read_reader_file()
        if reader_id in reader_list[0] :
            break
        else :
            print "未查到此读者id!!!"
    book_list = []
    print "请输入书籍id，按0结束:\n"
    while 1 :
        book_id = str(raw_input())
        if book_id == "0" :
            break
        book_list.append(book_id)
    arrears = bb.book_return(reader_id, book_list)
    print arrears
    if arrears >= 0.0 : 
        print "还书成功，应交罚款%.2f" % (arrears)
    else :
        print "查无此人!!!"
    raw_input("请按回车键继续")


#7 flag 1 界面操作
def get_booklist(flag = 0) :
    book_list = [""]
    b.operator_book_file(4, book_list)
    if b.search_book(0, book_list) == 0 :
        for i in xrange(1, len(book_list)) :
         "书本id:%s, 书名:%s, 作者:%s, 价钱:%s, 书本数量:%s, 书本剩余数量%s.\n" \
              % (book_list[i][0], book_list[i][1], book_list[i][2], book_list[i][3], \
                 book_list[i][4], book_list[i][5])
    else :
        print "库存中还未有书籍!!!"    
    if flag == 1 :
        raw_input("请按回车键继续")


#8
def add_reader() :
    reader_id = str(raw_input("请输入以下信息，*为必填项\n*请输入读者id:"))
    reader_name = str(raw_input("*请输入读者姓名:"))
    reader_address = str(raw_input("请输入读者地址:"))
    reader_phone = str(raw_input("请输入读者电话:"))
    reader_list = [reader_id, reader_name, reader_address, reader_phone, ""]
    r.add_reader(reader_list)
    print "添加读者%s %s成功" % (reader_list[3], reader_name)
    raw_input("请按回车键继续")


#9
def delete_reader() :
    reader_list = []
    r.show_reader_list(reader_list)
    for l in reader_list :
        print "%s\t" % (l)
    print "----------------------------"
    reader_id = str(raw_input("请输入要删除的读者id:"))
    reader_list = [reader_id, ""]
    if r.delete_reader(reader_list) == 0 :
        print "删除读者%s %s成功" % (reader_id, reader_list[1])
    else :
        print "未查到该读者信息"
    raw_input("请按回车键继续")


#10
def set_up() :
    os.system("cls")
    global flag
    while 1 :
        if flag == True :
            i = 0
        else :
            print "".center(50, "-")
            print "--------1、系统版本查询".ljust(30, "-")
            print "--------2、管理员密码修改/重置".ljust(30, "-")
            print "--------0、退出".ljust(30, "-")
            print "".center(50, "-")
            i = int(raw_input("请输入要操作的内容："))
        if i == 1:
            get_version()
        elif i == 2:
            modify_admin_password()
        elif i == 0:
            break
        else:
            continue
        

def operater_system() :
    global now_user
    global flag
    os.system("cls")
    while 1 :
        if flag == True :
            i = 0
            flag = False
        else :
            print "当前管理员:%s".center(50, "*") % (now_user)
            print "".center(50, "-")
            print "--------1、增加书籍".ljust(30, "-")
            print "--------2、删除书籍".ljust(30, "-")
            print "--------3、修改书籍信息".ljust(30, "-")
            print "--------4、书籍查询".ljust(30, "-")
            print "--------5、书籍借阅".ljust(30, "-")
            print "--------6、书籍归还".ljust(30, "-")
            print "--------7、列出所有在存书籍".ljust(30, "-")
            print "--------8、新增借阅者".ljust(30, "-")
            print "--------9、借阅者注销".ljust(30, "-")
            print "--------10、设置".ljust(30, "-")
            print "--------0、退出系统".ljust(30, "-")
            print "".center(50, "-")
            i = int(raw_input("请输入要操作的内容："))
        if i == 1 :
            add_book()
        elif i == 2 :
            delete_book()
        elif i == 3 :
            modify_book()
        elif i == 4 :
            search_book()
        elif i == 5 :
            borrow_book()
        elif i == 6 :
            return_book()
        elif i == 7 :
            get_booklist(1)
        elif i == 8 :
            add_reader()
        elif i == 9 :
            delete_reader()
        elif i == 10 :
            set_up()
        elif i == 0 :
            now_user = ""
            break
        else :
            continue

    
def main() :
    os.system("cls")
    while 1 :
        print "".center(50, "-")
        print "----------1、注册".ljust(30, "-")
        print "----------2、登录".ljust(30, "-")
        print "----------0、退出".ljust(30, "-")
        print "".center(50, "-")
        i = int(raw_input("请输入："))
        if i == 1 :
            register()
        elif i == 2 :
            login()
        elif i == 0 :
            break
        else :
            continue

if __name__ == "__main__" :
    os.system("cls")
    main()
