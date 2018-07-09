# Author: Alan
from interface import admin_interface
from lib import common
from conf import settings
import os
login_data={
    'name':'',
    'status':False
}

def login():
    if login_data['name']:
        print('禁止重复登录！')
        return False
    while True:
        name = input('请输入登录名：').strip()
        if name == 'q': return False
        pwd = input('请输入登录密码：').strip()
        if pwd == 'q': return False
        flag,message=common.login_action(name,pwd,'admin')
        print(message)
        print()
        if flag:
            login_data['name']=name
            login_data['status']=True
            return True


@common.login_auth('admin')
def create_campus():
    print('----------创建校区-------')
    while True :
        campus_name=input('请输入校区：').strip()
        if campus_name=='q':return False
        flag,message=admin_interface.create_campus(login_data['name'],campus_name)
        print(message)
        print()
        if flag:
            break

@common.login_auth('admin')
def check_campus():
    print('----------查看校区-------')
    admin_interface.check_campus()

@common.login_auth('admin')
def create_course():
    print('----------创建课程-------')
    print('请先选择校区')
    campus_list=admin_interface.check_campus()
    if not campus_list:
        return False
    while True:
        campus_id = input('请选择校区（编号）：').strip()
        if campus_id == 'q': return False
        if campus_id.isdigit() and int(campus_id)<len(campus_list):
            campus_id=int(campus_id)
            break
    while True :
        course_name=input('请输入课程：').strip()
        if course_name=='q':return False
        course_price = input('请输入课程价格：').strip()
        if course_price == 'q': return False
        course_period = input('请输入课程周期（天）：').strip()
        if course_period == 'q': return False
        if not course_price.isdigit() or not course_period.isdigit():
            print('输入有误')
            continue
        flag,message=admin_interface.create_course(login_data['name'],campus_list[campus_id],course_name,int(course_price),course_period)
        print(message)
        print()
        if flag:
            break

@common.login_auth('admin')
def check_course():
    print('----------查看课程-------')
    admin_interface.check_course()

@common.login_auth('admin')
def create_teacher():
    print('----------创建老师-------')
    print('请先选择校区')
    campus_list = admin_interface.check_campus()
    if not campus_list:
        return False
    while True:
        campus_id = input('请选择校区（编号）：').strip()
        if campus_id == 'q': return False
        if campus_id.isdigit() and int(campus_id) < len(campus_list):
            campus_id = int(campus_id)
            break
    while True:
        name = input('请输入老师登录名：').strip()
        if name == 'q': return False
        pwd = input('请输入老师登录密码：').strip()
        if pwd == 'q': return False

        flag, message = admin_interface.create_teacher(login_data['name'], campus_list[campus_id], name,
                                                      pwd,)
        print(message)
        print()
        if flag:
            break

@common.login_auth('admin')
def check_teacher():
    print('----------查看老师-------')
    admin_interface.check_teacher()

@common.login_auth('admin')
def create_classes():
    print('----------创建班级-------')
    print('请先选择校区')
    campus_list = admin_interface.check_campus()
    if not campus_list:
        return False
    while True:
        campus_id = input('请选择校区（编号）：').strip()
        if campus_id == 'q': return False
        if campus_id.isdigit() and int(campus_id) < len(campus_list):
            campus_id = int(campus_id)
            break

    print('请选择老师')
    teacher_list = admin_interface.check_teacher()
    if not teacher_list:
        return False
    while True:
        teacher_id = input('请选择老师（编号）：').strip()
        if teacher_id == 'q': return False
        if teacher_id.isdigit() and int(teacher_id) < len(teacher_list):
            teacher_id = int(teacher_id)
            break

    print('请选择课程')
    course_list = admin_interface.check_course()
    if not course_list:
        return False
    while True:
        course_id = input('请选择课程（编号）：').strip()
        if course_id == 'q': return False
        if course_id.isdigit() and int(course_id) < len(course_list):
            course_id = int(course_id)
            break

    while True:
        classes_name=input('请输入班级名称）：').strip()
        if classes_name == 'q': return False

        flag, message = admin_interface.create_classes(login_data['name'], campus_list[campus_id], course_list[course_id],
                                                       teacher_list[teacher_id],classes_name )
        print(message)
        print()
        if flag:
            break
@common.login_auth('admin')
def check_classes():
    print('----------查看班级-------')
    admin_interface.check_classes()

##############################邪恶的分割线#######################################
action_list = [
        login,
    create_campus,
    check_campus,
    create_course,
    check_course,
    create_teacher,
    check_teacher,
    create_classes,
    check_classes,
]
def admin_run():

    while True:
        print('''
            -----管理员界面-----
            0 登录
            1 创建校区
            2 查看校区
            3 创建课程
            4 查看课程
            5 创建老师
            6 查看老师
            7 创建班级
            8 查看班级
            ''')
        choice = input('请选择你的操作（输入对应编号即可）：').strip()
        if choice == 'q': return True
        if choice.isdigit() and int(choice) < len(action_list):
            num = int(choice)
            action_list[num]()
        else:
            print('输入有误')


if __name__ == '__main__':
    admin_run()