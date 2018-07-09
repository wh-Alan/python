# Author: Alan

import os,json,struct
from lib import struct_tcp,common
from  core import tcp_client
import hashlib

def register(name,pwd):
    conn=tcp_client.tcp_conn()
    header={
        'type':'admin',
        'action':'register'
    }
    # md5加密
    md5_obj = hashlib.md5()
    md5_obj.update(pwd.encode('utf-8'))
    pwd = md5_obj.hexdigest()
    data = {
        'name': name,
        'pwd': pwd
    }
    data_bytes=struct_tcp.pack_header(header,data)
    conn.send(data_bytes)

    res=common.receive_data(conn,'admin','register')
    if res:
        return True,res['msg']
    else:return False,'通信错误了'

def login(name,pwd):
    conn=tcp_client.tcp_conn()
    header={
        'type':'admin',
        'action':'login'
    }
    # md5加密
    md5_obj = hashlib.md5()
    md5_obj.update(pwd.encode('utf-8'))
    pwd=md5_obj.hexdigest()
    data={
        'name':name,
        'pwd':pwd
    }
    data_bytes=struct_tcp.pack_header(header,data)
    conn.send(data_bytes)

    res=common.receive_data(conn,'admin','login')
    if res:
        return res['status'],res['msg']
    else:return False,'通信错误了'

def upload_video(name,path,is_charge,cost,member_cost):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'upload_video'
    }
    if os.path.isfile(path):
        file_pathx,filename=os.path.split(path)
        file_size=os.path.getsize(path)
        md5_obj=hashlib.md5()
        md5_obj.update(str(file_size).encode('utf-8'))
        header['md5']=md5_obj.hexdigest()
        header['len']=file_size
        header['filename']=filename
        header['name']=name
        header['is_charge'] = is_charge
        header['cost'] = cost
        header['member_cost'] = member_cost
        header_bytes = json.dumps(header).encode('utf-8')

        header_len = len(header_bytes)
        header_len_bytes = struct.pack('i', header_len)
        conn.send(header_len_bytes)
        conn.send(header_bytes)
        res_TorF = common.receive_data(conn, 'admin', 'upload_video')
        if not res_TorF['status']:return False, res_TorF['msg']
        count=0
        with open(path,'rb') as f:
            for line in f:
                conn.send(line)
                count+=len(line)
                common.schedule(file_size,count)

        res = common.receive_data(conn, 'admin', 'upload_video')
        if res:
            return True, res['msg']
        else:
            return False, '通信错误了'

    return False, '文件不存在'

def get_video_list():
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'get_video_list'
    }
    data={
        'get_video_list':'get_video_list'
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)
    res = common.receive_data(conn, 'admin', 'get_video_list')
    return res['data']

def delete_video(name,id):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'delete_video'
    }
    data = {
        'id': id
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)

    res = common.receive_data(conn, 'admin', 'delete_video')
    if res:
        return True,res['msg']
    else:return False,'通信错误了'


def release_notice(name, content):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'release_notice'
    }
    data = {
        'content': content
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)

    res = common.receive_data(conn, 'admin', 'release_notice')
    if res:
        return True, res['msg']
    else:
        return False, '通信错误了'

def chech_capital(name):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'chech_capital'
    }
    data = {
        'chech_capital': 'chech_capital'
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)
    res = common.receive_data(conn, 'admin', 'chech_capital')
    return res['data']

def check_user():
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'check_user'
    }
    data = {
        'check_user': 'check_user'
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)
    res = common.receive_data(conn, 'admin', 'check_user')
    return res['data']

def manage_user(name,phone,is_lock):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'admin',
        'action': 'manage_user'
    }
    data = {
        'phone': phone,
        'is_lock': is_lock,
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)

    res = common.receive_data(conn, 'admin', 'manage_user')
    if res:
        return True, res['msg']
    else:
        return False, '通信错误了'