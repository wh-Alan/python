# Author: Alan
import re
from  lib import  common
from interface import user_interface,admin_interface
import time
login_data={
    'name':'',
    'info':{}
}

def register():
    print('------------注册----------')
    while True:
        phone = input('请输入手机号：').strip()
        if phone == 'q': break
        if not phone: continue
        if not phone.isdigit() or not re.findall('1[3|5|7|8]\d{9}',phone):
            print('手机号格式错误')
            continue
        pwd=input('请输入密码：').strip()
        if pwd == 'q': break
        if not pwd: continue

        flag,msg=user_interface.register(int(phone),pwd)
        print(msg)
        if flag:return True

def login():
    print('------------登录----------')
    while True:
        phone=input('请输入手机号：').strip()
        if phone == 'q': break
        if not phone: continue
        if not phone.isdigit() or not re.findall('1[3|5|7|8]\d{9}',phone):
            print('手机号格式错误')
            continue
        pwd=input('请输入密码：').strip()
        if pwd == 'q': break
        if not pwd: continue
        flag,msg,res=user_interface.login(int(phone),pwd)
        print(msg)
        if flag:
            login_data['name']=int(phone)
            login_data['info']=res['data']
            notice_list = user_interface.chech_notice(login_data['name'])
            print('最新公告：')
            if not notice_list['data']: return False
            print(notice_list['data'][-1][1])

            return True

@common.login_auth(auth_type='user')
def become_member():
    print('------------冲会员或充值----------')
    while True:
        money = input('充值金额：（若不是会员，自动扣50成为会员，如已是会员，则为充值）').strip()
        if money == 'q': break
        if not money or not money.isdigit(): continue

        flag,msg,res=user_interface.become_member(login_data['name'],int(money))
        print(msg,res)
        print('当前余额为：',res['money'][2])
        if flag:
            login_data['info'] = res['money']
            return True

@common.login_auth(auth_type='user')
def dwn_video():
    print('------------下载视频----------')
    video_list=admin_interface.get_video_list()
    if not video_list:
        print('暂无视频')
        return False

    print('id',  '路径', '价格', '会员价','是否收费','是否删除')
    video_list_id={}
    for i, l in enumerate(video_list):
        if l[-1]==1:continue
        video_list_id[l[0]]=l[4]
        print(l)
    while True:
        choice = input('请输入要下载视频id：').strip()
        if choice == 'q': break
        if not choice : continue
        if choice.isdigit() and int(choice) in video_list_id:
            if video_list_id[int(choice)]==0 and login_data['info'][3]==0:
                print('非会下载普通视频10秒广告，为了方便。。。')
                time.sleep(10)
            flag, msg = user_interface.dwn_video(login_data['name'],int(choice))
            print(msg)
            if flag:
                return True

@common.login_auth(auth_type='user')
def check_dwn_records():
    print('------------查看观影（下载）记录----------')
    dwn_records=user_interface.check_dwn_records(login_data['name'])
    print(dwn_records['msg'])
    if not dwn_records['data']:return False
    print('phone','user_id','当时价格','路径')
    for l in dwn_records['data']:
        print(login_data['name'],l)


@common.login_auth(auth_type='user')
def chech_notice():
    print('------------查看公告----------')
    notice_list=user_interface.chech_notice(login_data['name'])
    print(notice_list['msg'])
    if not notice_list['data']:
        print('暂无公告')
        return False
    print('id','content')
    for l in notice_list['data']:
        print(l)


action_list=[
    register,
    login,
    become_member,
    dwn_video,
    check_dwn_records,
    chech_notice
]
def run():
    print('------------管理员界面----------')
    print()
    while True:
        print('''
        0 注册
        1 登录
        2 冲会员或充值
        3 下载视频
        4 查看观影（下载）记录
        5 查看公告
        ''')
        res = input('请选择：').strip()
        if res == 'q': break
        if not res: continue
        if res.isdigit() and int(res) < len(action_list):
            res = int(res)
            action_list[res]()
        else:
            print('输入有误')


