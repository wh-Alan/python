# Author: Alan

import re
from  lib import  common
from  interface import admin_interface
login_data={
    'name':'',
    'info':{}
}

def register():
    print('------------注册----------')
    while True:
        name=input('请输入管理员名：').strip()
        if name == 'q': break
        if not name: continue
        pwd=input('请输入密码：').strip()
        if pwd == 'q': break
        if not pwd: continue
        flag,msg=admin_interface.register(name,pwd)
        print(msg)
        if flag:return True

def login():
    print('------------登录----------')
    while True:
        name=input('请输入管理员名：').strip()
        if name == 'q': break
        if not name: continue
        pwd=input('请输入密码：').strip()
        if pwd == 'q': break
        if not pwd: continue
        flag,msg=admin_interface.login(name,pwd)
        print(msg)
        if flag:
            login_data['name']=name
            return True

@common.login_auth(auth_type='admin')
def upload_video():
    print('------------上传视频----------')
    while True:
        path=input('请输入上传视频的路径：').strip()
        if path == 'q': break
        if not path: continue
        is_charge = input('是否收费：(0|1)').strip()
        if is_charge == 'q': break
        if not is_charge or is_charge!='0' and is_charge!='1': continue
        cost = input('请输入下载的价格：').strip()
        if cost == 'q': break
        if not cost or not cost.isdigit(): continue
        member_cost = input('请输入会员下载的价格：').strip()
        if member_cost == 'q': break
        if not member_cost or not member_cost.isdigit(): continue
        flag,msg=admin_interface.upload_video(login_data['name'],path,int(is_charge),round(int(cost),2),round(int(member_cost),2))
        print(msg)
        if flag:
            return True

@common.login_auth(auth_type='admin')
def delete_video():
    print('------------删除视频----------')

    video_list=admin_interface.get_video_list()
    if not video_list:
        print('暂无视频')
        return True
    print('id','链接','普通价格','会员价格','是否收费','是否删除')
    video_list_id=[]
    for i in video_list:
       if i[-1]==1:continue
       video_list_id.append(i[0])
       print(i)
    while True:
        choice = input('请输入要删除视频id：').strip()
        if choice == 'q': break
        if not choice : continue
        if choice.isdigit() and int(choice) in video_list_id:
            flag, msg = admin_interface.delete_video(login_data['name'],int(choice))
            print(msg)
            if flag:
                return True
@common.login_auth(auth_type='admin')
def release_notice():
    print('------------发布公告----------')
    while True:
        content = input('请输入公告内容：').strip()
        if content == 'q': break
        if not content : continue
        flag, msg = admin_interface.release_notice(login_data['name'],content)
        print(msg)
        if flag:
            return True

@common.login_auth(auth_type='admin')
def chech_capital():
    print('------------查看资金----------')
    data = admin_interface.chech_capital(login_data['name'])
    print('下载视频收到的资金','冲会员收到的资金（每位50）','合计')
    print(data[0],data[1]*50,data[1]*50+data[0])


@common.login_auth(auth_type='admin')
def check_user():
    print('------------查看用户----------')
    user_list = admin_interface.check_user()
    if not user_list:
        print('暂无用户')
        return True
    print('id','phone', 'money', 'is_member',  'is_delete')
    for l in user_list:
        print(l)

@common.login_auth(auth_type='admin')
def manage_user():

    print('------------管理用户----------')
    print('------------用户信息如下----------')
    user_list = admin_interface.check_user()
    if not user_list:
        print('暂无用户')
        return True
    print('id', 'phone', 'money', 'is_member', 'is_delete')
    for l in user_list:
        print(l)

    while True:
        is_lock = input('解除|锁定：(0|1)').strip()
        if is_lock == 'q': break
        if not is_lock or is_lock != '0' and is_lock != '1': continue
        phone = input('请输入用户手机号：').strip()
        if phone == 'q': break
        if not phone: continue
        if not phone.isdigit() or not re.findall('1[3|5|7|8]\d{9}',phone):
            print('手机号格式错误')
            continue
        flag, msg = admin_interface.manage_user(login_data['name'], int(phone),int(is_lock))
        print(msg)
        if flag:
            return True


action_list=[
    register,
    login,
    upload_video,
    delete_video,
    release_notice,
    chech_capital,
    check_user,
    manage_user,
]

def run():
    print('------------管理员界面----------')
    print()
    while True:
        print('''
        0 注册
        1 登录
        2 上传视频
        3 删除视频
        4 发布公告
        5 查看资金
        6 查看用户
        7 管理用户
        ''')
        res = input('请选择：').strip()
        if res == 'q': break
        if not res: continue
        if res.isdigit() and int(res) < len(action_list):
            res = int(res)
            action_list[res]()
        else:
            print('输入有误')



