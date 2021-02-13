#!/usr/bin/python
# -*- coding:gbk -*-

import os
from admin import Admin
from book import Book
import reader as r
import book_borrow as bb

now_user = ""
system_version = "1.0.0.1-201210211"
a = Admin()
con = a.get_db_con()
b = Book(con)


# ����Աע��
def register():
    while 1:
        user_id = input("�������û�id:")
        flag = a.search_in_admin_db([user_id])
        if flag == 0:
            break
        else:
            print("���û�id�Ѵ��ڣ������!!!")
    user_name = input("�������û���:")
    while 1:
        user_password = input("����������:")
        user_password_again = input("���ٴ���������:")
        if user_password == user_password_again:
            a.register_in_admin_db([user_id, user_name, user_password])
            break
        else:
            print("�����������벻һ�£�����������!!!")
            continue
    print("ע��ɹ�->->-> �û�����%s��id��%s" % (user_name, user_id))
    input("�밴�س�������")
    os.system("cls")
    

# ����Ա��¼
def login():
    global now_user
    user_id = input("�������û�id:")
    while 1:
        user_password = input("����������:")
        user_list = [user_id, user_password]
        flag = a.search_in_admin_db(user_list)
        if flag == 1:
            now_user = user_list[2]
            operator_system()
            break
        elif flag == -1:
            print("�����������������!!!")
            continue
        elif flag == 0:
            print("���޴��û�!!!")
            break


# �汾��ѯ
def get_version():
    print("sys:%s" % system_version)
    input("�밴�س�������")


# �޸Ĺ���Ա����
def modify_in_admin_db_password():
    global now_user
    user_id = str(input("�������û�id��"))
    if a.search_in_admin_db([user_id]) == 0:
        print("���޴��û�!!!")
        return 
    user_password = str(input("�����뵱ǰ����(��Ϊ�գ�����������)��"))
    if user_password != "":
        while 1:
            user_new_password = str(input("�����������룺"))
            if user_password == user_new_password:
                print("�������벻����ͬ!!!")
                continue
            user_new_password_again = str(input("���������������룺"))
            if user_new_password == user_new_password_again:
                a.modify_in_admin_db(0, [user_id, user_new_password])
                print("%s�����޸ĳɹ�" % user_id)
                break
            else:
                print("�������벻һ�£�����������!!!")
    else:
        user_name = str(input("�������û�����"))
        if a.search_in_admin_db([user_id, "", user_name]) == 0:
            print("�û����������!!!")
        else:
            a.modify_in_admin_db(1, [user_id])
            print("%s�������óɹ�" % user_id)

    if user_name == now_user:
        now_user = ""
        print("��ǰ�û������Ѹı䣬�����µ�¼!!!")
        flag = True
        input("�밴�س�������")
    else:
        input("�밴�س�������")


# 1
def add_book():
    book_id = str(input("�������鼮id��"))
    book_name = str(input("������������"))
    book_author = str(input("���������ߣ�"))
    book_money = float(input("�������鱾��Ǯ��"))
    book_num = int(input("�������鱾��������"))
    book_remain_num = book_num
    book_info = [book_id, book_name, book_author, book_money, book_num, book_remain_num]
    flag = b.add_book(book_info)
    if flag == 0:
        print("�鱾%s��ӳɹ�, ͼ������:%s, ͼ��id:%s, ͼ���Ǯ:%s, ͼ������:%s"
              % (book_name, book_author, book_id, book_money, book_num))
    elif flag == 1:
        print("�鱾%s��ӿ��ɹ�, ͼ������:%s, ͼ��id:%s, ͼ���Ǯ:%s, ͼ������:%s"
              % (book_name, book_author, book_id, book_money, book_num))
    else:
        print("���ʧ��!!!")
    input("�밴�س�������")


# 2
def delete_book():
    get_booklist()
    print("----------------------------")
    book_id = str(input("������Ҫɾ�����鼮id:"))
    if b.delete_book(book_id) == 0:
        print("�鱾%sɾ���ɹ�" % book_id)
    else:
        print("δ�ڿ�����ҵ�����!!!")
    input("�밴�س�������")


# 3
def modify_book():
    get_booklist()
    print("----------------------------")
    book_name = str(input("������Ҫ��ѯ�鼮id/����/����:"))
    type_num = int(input("��������Ҫ�޸ĵ����ݣ�1.���� 2.���� 3.��Ǯ 4.�鱾���� 5.�鱾ʣ������\n"))
    string = str(input("�������޸�ֵ"))
    old_string = ""
    temp = ""
    if type_num == 1:
        temp = "book_name"
    elif type_num == 2:
        temp = "book_author"
    elif type_num == 3:
        temp = "book_money"
    elif type_num == 4:
        temp = "book_num"
    elif type_num == 5:
        temp = "book_remain_num"
    if b.modify_book([book_name, temp, string, old_string]) == 0 :
        print("�޸�%s����%s %s->%s �ɹ�" % (book_name, temp, old_string, string))
    else:
        print("δ�ڿ�����ҵ�����!!!")
    input("�밴�س�������")


# 4
def search_book():
    print("----------------------------")
    book_name = str(input("������Ҫ��ѯ�鼮id/����/����:"))
    book_list = [book_name, "", "", "", "", ""]
    if b.search_book(1, book_list) == 0:
        print("�鱾id:%s, ����:%s, ����:%s, ��Ǯ:%s, �鱾����:%s, �鱾ʣ������%s.\n"
              % (book_list[0], book_list[1], book_list[2], book_list[3], book_list[4], book_list[5]))
    else:
        print("δ�ڿ�����ҵ�����!!!")
    input("�밴�س�������")


# 5
def borrow_book():
    # ����id
    while 1:
        reader_id = str(input("���������id:"))
        reader_list = []
        r.show_reader_list(reader_list)
        if reader_id in reader_list[0]:
            break
        else:
            temp = str(input("δ�鵽�˶���id!!!\n��0�������룬�������˳�����:"))
            if temp == "0":
                continue
            else:
                return
    # �����鼮
    book_list = []
    print("�������鼮id����0����:\n")
    while 1:
        book_id = str(input())
        if book_id == "0":
            break
        book_list.append(book_id)
        if len(book_list) >= 8:
            print("���鳬��8��,ǰ8�����Ƚ��!!!")
            break
    # ��ѯ�鼮�Ƿ���ڼ����
    book_temp = []
    b.search_book(0, book_temp)
    for i in range(0, len(book_list)):
        if book_list[i] not in book_temp[0]:
            book_list.pop(i)
    for i in range(0, len(book_list)):
        for book in book_temp:
            if book_list[i] == book[0] and book[5] == 0:
                book_list.pop(i)
                break
    bb.book_borrow(reader_id, book_list)
    print("����ɹ�")
    input("�밴�س�������")
    

# 6
def return_book() :
    while 1 :
        reader_id = str(input("���������id:"))
        reader_list = r.read_reader_file()
        if reader_id in reader_list[0] :
            break
        else :
            print("δ�鵽�˶���id!!!")
    book_list = []
    print("�������鼮id����0����:\n")
    while 1 :
        book_id = str(input())
        if book_id == "0" :
            break
        book_list.append(book_id)
    arrears = bb.book_return(reader_id, book_list)
    print(arrears)
    if arrears >= 0.0 : 
        print("����ɹ���Ӧ������%.2f" % (arrears))
    else :
        print("���޴���!!!")
    input("�밴�س�������")


# 7 flag 1 �������
def get_booklist(flag=0):
    book_list = [""]
    if b.search_book(0, book_list) == 0:
        for i in range(1, len(book_list)) :
            print("�鱾id:%s, ����:%s, ����:%s, ��Ǯ:%s, �鱾����:%s, �鱾ʣ������%s.\n"
                  % (book_list[i][0], book_list[i][1], book_list[i][2], book_list[i][3],
                     book_list[i][4], book_list[i][5]))
    else:
        print("����л�δ���鼮!!!")
    if flag == 1:
        input("�밴�س�������")


# 8
def add_reader():
    reader_id = str(input("������������Ϣ��*Ϊ������\n*���������id:"))
    reader_name = str(input("*�������������:"))
    reader_address = str(input("��������ߵ�ַ:"))
    reader_phone = str(input("��������ߵ绰:"))
    reader_list = [reader_id, reader_name, reader_address, reader_phone, ""]
    r.add_reader(reader_list)
    print("��Ӷ���%s %s�ɹ�" % (reader_list[3], reader_name))
    input("�밴�س�������")


# 9
def delete_reader():
    reader_list = []
    r.show_reader_list(reader_list)
    for rl in reader_list:
        print("%s\t" % rl)
    print("----------------------------")
    reader_id = str(input("������Ҫɾ���Ķ���id:"))
    reader_list = [reader_id, ""]
    if r.delete_reader(reader_list) == 0:
        print("ɾ������%s %s�ɹ�" % (reader_id, reader_list[1]))
    else:
        print("δ�鵽�ö�����Ϣ")
    input("�밴�س�������")


# 10
def set_up():
    os.system("cls")
    while 1:
        print("".center(50, "-"))
        print("--------1��ϵͳ�汾��ѯ".ljust(30, "-"))
        print("--------2������Ա�����޸�/����".ljust(30, "-"))
        print("--------0���˳�".ljust(30, "-"))
        print("".center(50, "-"))
        i = int(input("������Ҫ���������ݣ�"))
        if i == 1:
            get_version()
        elif i == 2:
            modify_in_admin_db_password()
        elif i == 0:
            break
        else:
            continue
        

def operator_system():
    global now_user
    os.system("cls")
    while 1:
        print("��ǰ����Ա:%s".center(50, "*") % now_user)
        print("".center(50, "-"))
        print("--------1�������鼮".ljust(30, "-"))
        print("--------2��ɾ���鼮".ljust(30, "-"))
        print("--------3���޸��鼮��Ϣ".ljust(30, "-"))
        print("--------4���鼮��ѯ".ljust(30, "-"))
        print("--------5���鼮����".ljust(30, "-"))
        print("--------6���鼮�黹".ljust(30, "-"))
        print("--------7���г������ڴ��鼮".ljust(30, "-"))
        print("--------8������������".ljust(30, "-"))
        print("--------9��������ע��".ljust(30, "-"))
        print("--------10������".ljust(30, "-"))
        print("--------0���˳�ϵͳ".ljust(30, "-"))
        print("".center(50, "-"))
        i = int(input("������Ҫ���������ݣ�"))
        if i == 1:
            add_book()
        elif i == 2:
            delete_book()
        elif i == 3:
            modify_book()
        elif i == 4:
            search_book()
        elif i == 5:
            borrow_book()
        elif i == 6:
            return_book()
        elif i == 7:
            get_booklist(1)
        elif i == 8:
            add_reader()
        elif i == 9:
            delete_reader()
        elif i == 10:
            set_up()
        elif i == 0:
            now_user = ""
            break
        else:
            continue

    
def main():
    os.system("cls")
    while 1:
        print("".center(50, "-"))
        print("----------1��ע��".ljust(30, "-"))
        print("----------2����¼".ljust(30, "-"))
        print("----------0���˳�".ljust(30, "-"))
        print("".center(50, "-"))
        i = int(input("�����룺"))
        if i == 1:
            register()
        elif i == 2:
            login()
        elif i == 0:
            del a
            break
        else:
            continue


if __name__ == "__main__":
    os.system("cls")
    main()
