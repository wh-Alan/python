# Author:Alan

from db import handle_db
from conf import settings
import os


def check_classes(name):
    obj=handle_db.Teacher.get_obj(name)
    if not obj.classes_list:
        print('暂无选择班级进行任课')
        return []
    for i,v in enumerate(obj.classes_list):
        print('编号：%s'%i,'班级：%s'%v)

    print()
    return obj.classes_list

def check_classes_info(name):
    obj = handle_db.Teacher.get_obj(name)
    if not obj.classes_list:
        print('暂无选择班级进行任课')
        return []
    for i,v in enumerate(obj.classes_list):
        classes_obj=handle_db.Classes.get_obj(v)
        print('编号：%s'%i,'班级：%s'%v,'学员列表：%s'%classes_obj.student_list)

def upadte_stu_grade(name,classes_name,student_name,score):
    obj=handle_db.Student.get_obj(student_name)
    obj.update_grade(classes_name,score)
    return True,'修改成功'