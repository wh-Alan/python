# Author: Alan

import os,json,struct
from conf import settings
from lib import struct_tcp,common
from  core import tcp_client
import hashlib

def register(phone,pwd):
    conn=tcp_client.tcp_conn()
    header={
        'type':'user',
        'action':'register'
    }
    # md5加密
    md5_obj = hashlib.md5()
    md5_obj.update(pwd.encode('utf-8'))
    pwd = md5_obj.hexdigest()
    data = {
        'phone': phone,
        'pwd': pwd
    }
    data_bytes=struct_tcp.pack_header(header,data)
    conn.send(data_bytes)

    res=common.receive_data(conn,'user','register')
    if res:
        return True,res['msg']
    else:return False,'通信错误了'

def login(phone,pwd):
    conn=tcp_client.tcp_conn()
    header={
        'type':'user',
        'action':'login'
    }
    # md5加密
    md5_obj = hashlib.md5()
    md5_obj.update(pwd.encode('utf-8'))
    pwd=md5_obj.hexdigest()
    data={
        'phone':phone,
        'pwd':pwd
    }
    data_bytes=struct_tcp.pack_header(header,data)
    conn.send(data_bytes)

    res=common.receive_data(conn,'user','login')
    if res:
        return res['status'],res['msg'],res
    else:return False,'通信错误了'

def become_member(phone,money):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'user',
        'action': 'become_member'
    }
    data = {
        'phone': phone,
        'money': money
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)

    res = common.receive_data(conn, 'user', 'become_member')
    if res:
        return res['status'], res['msg'], res
    else:
        return False, '通信错误了'

def dwn_video(phone,id):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'user',
        'action': 'dwn_video'
    }
    data = {
        'phone': phone,
        'id': id
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)
    T_F=conn.recv(1).decode('utf-8')
    if T_F=='0':return False,'余额不足'
    re_header_len_bytes = conn.recv(4)
    re_header_len = struct_tcp.unpack_header_len(re_header_len_bytes)

    re_header_bytes = conn.recv(re_header_len)
    re_header = struct_tcp.decode_header_bytes_or_data_bytes(re_header_bytes)

    recv_size = 0
    video_path1 = os.path.join(settings.Videos_path, re_header['filename'])

    with open(video_path1, 'wb') as f:
        while recv_size < re_header['filesize']:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_size += len(recv_data)
            common.schedule(re_header['filesize'], recv_size)
        f.flush()
    file_size1 = os.path.getsize(video_path1)
    md5_obj = hashlib.md5()
    md5_obj.update(str(file_size1).encode('utf-8'))
    if re_header['md5'] == md5_obj.hexdigest():
        return True,'下载成功'
    else:
        return False,'文件不完整或被篡改'

def check_dwn_records(phone):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'user',
        'action': 'check_dwn_records'
    }
    data = {
        'phone': phone
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)

    res = common.receive_data(conn, 'user', 'check_dwn_records')
    if res:
        return  res
    else:
        print('通信错误了')
        return []
def chech_notice(phone):
    conn = tcp_client.tcp_conn()
    header = {
        'type': 'user',
        'action': 'chech_notice'
    }
    data = {
        'phone': phone
    }
    data_bytes = struct_tcp.pack_header(header, data)
    conn.send(data_bytes)

    res = common.receive_data(conn, 'user', 'chech_notice')
    if res:
        return res
    else:
        return '通信错误了'