# Author: Alan
from db import handle_db
from conf import settings
import os

def create_campus(admin_name,campus_name):
    obj=handle_db.Campus.get_obj(campus_name)
    if not obj:
        obj=handle_db.Admin.get_obj(admin_name)
        obj.create_campus(campus_name)
        return True,'创建校区成功'
    return False,'已存在此校区'

def check_campus():
    path=os.path.join(settings.DB_PATH,'campus')
    if not os.path.exists(path):
        print('暂无校区')
        return []
    campus_list=os.listdir(path)
    for i,v in enumerate(campus_list):
        print(i,v,end='  ')
        print()
    print()
    print()
    return campus_list

def create_course(admin_name,campus_name,course_name,course_price,course_period):
    obj = handle_db.Course.get_obj(course_name)
    if not obj:
        obj = handle_db.Admin.get_obj(admin_name)
        obj.create_course(campus_name,course_name,course_price,course_period)
        return True, '创建课程成功'
    return False, '已存在此课程'

def check_course():
    path = os.path.join(settings.DB_PATH, 'course')
    if not os.path.exists(path):
        print('暂无课程')
        return []
    course_list = os.listdir(path)
    for i, v in enumerate(course_list):
        obj=handle_db.Course.get_obj(v)
        print('编号：%s'%i,'课程名：%s'%v, '价格：%s'%obj.price,'周期：%s天'%obj.period,end='  ')
        print()
    print()
    print()
    return course_list

def create_teacher(admin_name,campus_name,name,pwd):
    obj = handle_db.Teacher.get_obj(name)
    if not obj:
        obj = handle_db.Admin.get_obj(admin_name)
        obj.create_teacher(campus_name, name, pwd,)
        return True, '创建老师成功'
    return False, '已存在此老师'

def check_teacher():
    path = os.path.join(settings.DB_PATH, 'teacher')
    if not os.path.exists(path):
        print('暂无老师')
        return []
    teacher_list = os.listdir(path)
    for i, v in enumerate(teacher_list):
        print('编号：%s'%i,'老师登录名：%s'%v,end='  ')
        print()
    print()
    print()
    return teacher_list

def create_classes(admin_name,campus_name,course_name,teacher_name,classes_name):
    obj = handle_db.Classes.get_obj(classes_name)
    teacher_obj=handle_db.Teacher.get_obj(teacher_name)
    if classes_name in teacher_obj.classes_list:
        return False,'此老师已经选择过此班级'

    if not obj:
        obj = handle_db.Admin.get_obj(admin_name)
        obj.create_classes(campus_name,teacher_name,course_name,classes_name )
        teacher_obj.add_classes(classes_name)
        return True, '创建班级成功'
    return False, '已存在此班级'

def check_classes():
    path = os.path.join(settings.DB_PATH, 'classes')
    if not os.path.exists(path):
        print('暂无班级')
        return []
    classes_list = os.listdir(path)
    for i, v in enumerate(classes_list):
        obj=handle_db.Classes.get_obj(v)
        print('编号：%s'%i,'班级：%s'%v,'课程：%s'%obj.course_name,'老师：%s'%obj.teacher_name,end='  ')
        print()

    print()
    return classes_list