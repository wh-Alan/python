# Author: Alan

from core import admin
from core import student
from core import teacher
func_dic = {
    '1': admin.admin_run,
    '2': teacher.teacher_run,
    '3': student.student_run
}


def run():
    while True:
        print('''
        请选择登录角色：
        1、管理员视图
        2、老师视图
        3、学生视图

        ''')
        choice = input('please choice>>:').strip()
        if choice == 'q': break
        if choice not in func_dic: continue

        func_dic[choice]()