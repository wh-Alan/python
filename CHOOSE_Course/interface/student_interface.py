# Author:Alan
from db import handle_db
from conf import settings
import os

def register(name, pwd):
    obj = handle_db.Student.get_obj(name)
    if not obj:
        obj = handle_db.Student(name,pwd)
        return  True,'注册成功'
    return False,'登录名已存在'

def choose_classes(name,classes_name):
    stu_obj=handle_db.Student.get_obj(name)
    classes_obj=handle_db.Classes.get_obj(classes_name)
    course_obj=handle_db.Course.get_obj(classes_obj.course_name)
    if stu_obj.choose_classes(classes_name,course_obj.price):
        classes_obj.add_student(name)
        return True,'选择成功'
    return False,'已选了此班级'

def check_classes(name):
    stu_obj = handle_db.Student.get_obj(name)
    if not stu_obj.classes_list:
        print('没有选择班级')
        return []
    for i,v in enumerate(stu_obj.classes_list):
        classes_obj=handle_db.Classes.get_obj(v)
        print('编号：%s' % i, '班级：%s' % v, '课程：%s' % classes_obj.course_name, '老师：%s' % classes_obj.teacher_name,
        '已缴清' if stu_obj.cost[v]==0 else '未交费：%s'%stu_obj.cost[v],end='  ')
        print()
    print()
    return stu_obj.classes_list

def pay_to(name,classes_name,money):
    stu_obj = handle_db.Student.get_obj(name)
    if stu_obj.cost[classes_name]==0:
        return False,'已经缴清了'
    elif stu_obj.cost[classes_name]-money>0:
        return False,'钱不够'
    elif stu_obj.cost[classes_name]-money<0:
        return False,'给多了'
    else:
        stu_obj.pay_to(classes_name,money)
        return True,'缴费成功'
def check_grade(name):
    stu_obj = handle_db.Student.get_obj(name)
    if not stu_obj.grade:
        print('没有选择班级，暂无成绩')
        return {}
    for i in stu_obj.grade:
        print('班级：%s'%i,'成绩：%s'%stu_obj.grade[i])
    return stu_obj.grade