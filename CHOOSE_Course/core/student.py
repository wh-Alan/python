# Author: Alan
from interface import student_interface,admin_interface
from lib import common

login_data={
    'name':'',
    'status':False
}
def register():
    print('----------注册---------')
    while True:
        name = input('请输入登录名：').strip()
        if name == 'q': return False
        pwd = input('请输入登录密码：').strip()
        if pwd == 'q': return False
        flag, message = student_interface.register(name, pwd)
        print(message)
        print()
        if flag:break

def login():
    print('----------登录---------')
    if login_data['name']:
        print('禁止重复登录！')
        return False
    while True:
        name = input('请输入登录名：').strip()
        if name == 'q': return False
        pwd = input('请输入登录密码：').strip()
        if pwd == 'q': return False
        flag,message=common.login_action(name,pwd,'student')
        print(message)
        print()
        if flag:
            login_data['name']=name
            login_data['status']=True
            return True


@common.login_auth('student')
def choose_classes():
    print('----------选择班级-------')

    classes_list=admin_interface.check_classes()
    if not classes_list:return False
    while True:
        classes_id=input('请选择班级（编号）：').strip()
        if classes_id=='q':return False
        if classes_id.isdigit() and int(classes_id)<len(classes_list):
            flag, message = student_interface.choose_classes(login_data['name'],classes_list[int(classes_id)])
            print(message)
            print()
            if flag:break

@common.login_auth('student')
def check_classes():
    print('----------查看班级---------')
    student_interface.check_classes(login_data['name'])

@common.login_auth('student')
def pay_to():
    print('----------交学费---------')
    classes_list=student_interface.check_classes(login_data['name'])
    if not classes_list:return False

    while True:
        classes_id = input('请选择班级（编号）进行缴费：').strip()
        if classes_id == 'q': return False
        money=input('请输入缴费的金额：').strip()
        if money == 'q': return False
        if classes_id.isdigit() and money.isdigit()  and int(classes_id) < len(classes_list):
            flag, message = student_interface.pay_to(login_data['name'], classes_list[int(classes_id)],int(money))
            print(message)
            print()
            if flag: break
        print('输入有误')

@common.login_auth('student')
def check_grade():
    print('----------查看成绩---------')
    student_interface.check_grade(login_data['name'])
##############################邪恶的分割线#######################################
action_list = [
    register,
    login,
    choose_classes,
    check_classes,
    pay_to,
    check_grade
]
def student_run():

    while True:
        print('''
           -----学生界面-----
           0 注册
           1 登录
           2 选择班级
           3 查看班级
           4 交学费
           5 查看成绩
           ''')
        choice = input('请选择你的操作（输入对应编号即可）：').strip()
        if choice == 'q': return True
        if choice.isdigit() and int(choice) < len(action_list):
            num = int(choice)
            action_list[num]()
        else:
            print('输入有误')


if __name__ == '__main__':
    student_run()