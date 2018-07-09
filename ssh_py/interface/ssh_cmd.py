# Author: Alan
import re
from lib import common
from conf import settings
from core import thread_x
from core import paramiko_x

def first_deal(cmd):
    #初步处理命令
    data={}
    if cmd.find('-cmd')>-1:
        res=cmd.split('-cmd')[0].strip()
        data['cmd'] = cmd.split('-cmd')[1].strip(' "')
    elif cmd.find('-action')>-1:
        res = cmd.split('-action')[0]
        data['cmd'] = cmd.split('-action')[1].strip(' "')
    else:
        return  {}

    if res.find('-g')>-1:
        data['g']=res.split('-g')[1].strip()
        res=res.split('-g')[0].strip()
    else:data['g']=''

    if res.find('-h')>-1:
        data['h']=res.split('-h')[1].strip()
    else:data['h']=''

    if not data['g'] and not data['h']:return {}

    return data

def second_deal(data):
    #得到所有主机地址
    l = []
    res1=[]
    if data['h']:
        res1=data['h'].strip().split(',')
    if data['g']:

        res2 = data['g'].strip().split(',')
        for i in res2:
            h_str=common.get_filed_ini(settings.HOST_INI_PATH, i)
            if h_str:
                print(i, '不存在')
                l+=h_str[0][1].split(',')
    res=res1+l
    return list(set(res))

def third_deal(data):
    #处理命令
    cmd=data['cmd']
    if cmd.startswith('put'):
        res=re.findall('put\s+\-local(.*?)\-remote(.*)',cmd)
        if res:
            data['local']=res[0][0].strip()
            data['remote']=res[0][1].strip()
            data['type']='put'
        else:
            data['type']=''
        return data
    if cmd.startswith('get'):
        res=re.findall('get\s+\-remote(.*?)\-local(.*)',cmd)
        if res:
            data['local']=res[0][1].strip()
            data['remote']=res[0][0].strip()
            data['type']='get'
        else:
            data['type']=''
        return data
    else:
        data['type']='cmd'
        return data

def deal_cmd(cmd=''):
    #处理命令并调用相应的执行函数
    res=first_deal(cmd)
    if not res:
        print('输入格式有误')
        return False
    res['host']=second_deal(res)
    res=third_deal(res)
    print('命令有用信息>>>>',res)
    if res['type']:
        #开启线程
        for i in res['host']:
            host_data=common.get_filed_ini(settings.HOST_INI_PATH,i)
            if not host_data:
                print(i,'不存在')
                continue
            send_data={}
            send_data['hostname']=host_data[0][1]
            send_data['port']=host_data[1][1]
            send_data['username']=host_data[2][1]
            send_data['password']=host_data[3][1]
            if res['type'] == 'cmd':
                send_data['cmd']=res['cmd']
                thread_x.open_thread(paramiko_x.execute_cmd,res['type'],send_data)
            else:
                send_data['local'] = 'E:\\a.txt'
                send_data['remote'] = res['remote']
                send_data['type'] = res['type']
                thread_x.open_thread(paramiko_x.execute_action,res['type'],send_data)
