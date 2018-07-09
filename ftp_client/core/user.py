# Author: Alan
from interface import loginx
from interface import registerx
from  interface import uploadx
from  interface import downloadx
from  interface import mk_dirx
from  interface import check_filex
from  interface import change_dirx
from core import client


login_data={
    'name':'',
    'data':{},
    'now_dir':[]
}

def auth(func):
    #装饰器
    def wrapper(*args, **kwargs):
        if not login_data['name']:
            print('请先登录!')
            if not login(): return False
        func(*args, **kwargs)
    return wrapper

def register():
    print('-------------注册------------')
    while True:
        name=input('请输入登录名：').strip()
        if name=="q":break
        pwd = input('请输入密码：').strip()
        if pwd == "q": break
        flag,msg=registerx.register(name,pwd,client.client)
        print(msg)
        print()
        if flag:break

def login():
    print('-------------登录------------')
    while True:
        name=input('请输入登录名：').strip()
        if name=="q":return False
        pwd = input('请输入密码：').strip()
        if pwd == "q": return False
        flag,msg,res_all=loginx.login(name,pwd,client.client)
        print(msg)
        print()
        if flag:
            print('当前文件夹下的目录')
            print(res_all['mydir'])

            print('当前路径')
            print(res_all['now_dir'])

            login_data['name']=name
            login_data['data']=res_all
            login_data['now_dir']=res_all['now_dir']
            return True
@auth
def change_dir():
    #切换目录
    print('-------------切换目录------------')
    while True:
        flag, msg, res_all = check_filex.check_file(login_data['now_dir'], login_data['name'], login_data['data'],
                                                    client.client)
        print(msg)
        print()
        if flag:
            print(res_all['data'])

        path_name = input('请输入要切换目录：（以当前路径为准，b返回上一级）').strip()
        if path_name == "q": return False
        flag, msg, res_all = change_dirx.change_dir(login_data['now_dir'],login_data['name'],login_data['data'], path_name, client.client)
        print(msg)
        print()
        if flag:login_data['now_dir'].append(path_name)#改变当前路径

@auth
def upload():
    print('-------------上传------------')
    while True:
        path = input('请输入上传文件的路径：').strip()
        if path == "q": return False
        flag, msg, res_all = uploadx.upload(login_data['now_dir'],login_data['name'],login_data['data'], path, client.client)
        print(msg)
        print()
        if flag:
            break
@auth
def download():
    print('-------------下载------------')
    while True:
        filename = input('请输入要下载的文件名：').strip()
        if filename == "q": return False
        flag, msg, res_all = downloadx.download(login_data['now_dir'], login_data['name'], login_data['data'], filename,
                                            client.client)
        print(msg)
        print()
        if flag:
            break
@auth
def check_file():
    print('-------------查看目录下的文件------------')
    flag, msg, res_all = check_filex.check_file(login_data['now_dir'], login_data['name'], login_data['data'],
                                        client.client)
    print(msg)
    print()
    if flag:
        print(res_all['data'])

@auth
def mk_dir():
    print('-------------创建文件夹------------')
    while True:
        dirname = input('请输入要创建文件夹的名称：').strip()
        if dirname == "q": return False
        flag, msg, res_all = mk_dirx.mk_dir(login_data['now_dir'], login_data['name'], login_data['data'], dirname,
                                            client.client)
        print(msg)
        print()
        if flag:
            break


action_list=[
            ['注册',register],
            ['登录',login],
            ['切换目录',change_dir],
            ['上传',upload],
            ['下载',download],
            ['查看目录下的文件',check_file],
            ['创建文件夹',mk_dir],

        ]

def run():

    while True:
        print('------------ftp客户端---------')
        for i, v in enumerate(action_list):
            print(i, v[0])
        choice = input('请选择你的操作（输入对应编号即可）：').strip()
        if choice == 'q': return True
        if choice.isdigit() and int(choice) < len(action_list):
            num = int(choice)
            action_list[num][1]()
        else:
            print('输入有误')
if __name__ == '__main__':
    run()