# Author: Alan
from interface import teacher_interface
from lib import common

from  db import handle_db
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
        flag,message=common.login_action(name,pwd,'teacher')
        print(message)
        print()
        if flag:
            login_data['name']=name
            login_data['status']=True
            return True


@common.login_auth('teacher')
def choose_lesson():
    print('----------选择上课-------')
    classes_list=teacher_interface.check_classes(login_data['name'])
    if not classes_list:return False

    while True:
        classes_id = input('请选择班级（编号）：').strip()
        if classes_id == 'q': return False
        if classes_id.isdigit() and int(classes_id)<len(classes_list):
            print('选择成功')
            print('可以去上课了！！！')
            break

        print('输入有误')

@common.login_auth('teacher')
def check_classes_info():
    print('----------查看班级信息-------')
    teacher_interface.check_classes_info(login_data['name'])

@common.login_auth('teacher')
def upadte_stu_grade():
    print('----------修改学生成绩-------')
    print('你任课的班级如下')
    classes_list=teacher_interface.check_classes(login_data['name'])
    if not classes_list:return False
    while True:
        classes_id = input('请选择班级（编号）：').strip()
        if classes_id == 'q': return False
        if classes_id.isdigit() and int(classes_id) < len(classes_list):
            classes_id=int(classes_id)
            classes_name=classes_list[classes_id]
            break
        print('输入有误')
    classes_obj=handle_db.Classes.get_obj(classes_name)
    if not classes_obj.student_list:
        print('此班级暂无学生')
        return False
    for i,v in enumerate(classes_obj.student_list):
        stu_obj=handle_db.Student.get_obj(v)
        print('编号：%s' % i, '学员：%s' % v,'成绩：%s'%stu_obj.grade[classes_name])

    while True:
        stu_id = input('请选择学员（编号）：').strip()
        if stu_id == 'q': return False
        if stu_id.isdigit() and int(stu_id) < len(classes_obj.student_list):
            stu_id=int(stu_id)
            stu_name=classes_obj.student_list[stu_id]
            break
        print('输入有误')

    while True:
        score = input('请输入新的成绩：').strip()
        if score == 'q': return False
        if score.isdigit():
            flag, message=teacher_interface.upadte_stu_grade(login_data['name'], classes_name, stu_name, score)
            print(message)
            print()
            if flag:
                return True
        print('输入有误')
##############################邪恶的分割线#######################################

action_list = [
    login,
    choose_lesson,
    check_classes_info,
    upadte_stu_grade,

]
def teacher_run():
    while True:
        print('''
            -----老师界面-----
            0 登录
            1 选择上课
            2 查看班级信息
            3 修改学生成绩
            ''')
        choice = input('请选择你的操作（输入对应编号即可）：').strip()
        if choice == 'q': return True
        if choice.isdigit() and int(choice) < len(action_list):
            num = int(choice)
            action_list[num]()
        else:
            print('输入有误')


if __name__ == '__main__':
    teacher_run()