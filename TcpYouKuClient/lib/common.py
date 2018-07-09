# Author: Alan

from lib import struct_tcp

def login_auth(auth_type):
    #带参认证登录装饰器
    from core import admin,user
    def auth(func):
        def wrapper(*args,**kwargs):
            if auth_type=='admin':
                if not admin.login_data['name']:
                    print('请先登录')
                    if not admin.login(): return False
            if auth_type=='user':
                if not user.login_data['name']:
                    print('请先登录')
                    if not user.login():return False

            return func(*args,**kwargs)
        return wrapper
    return  auth


def receive_data(conn,type,action):
    #接收数据，除了上传和下载
    re_header_len_bytes = conn.recv(4)
    re_header_len = struct_tcp.unpack_header_len(re_header_len_bytes)

    re_header_bytes = conn.recv(re_header_len)
    re_header = struct_tcp.decode_header_bytes_or_data_bytes(re_header_bytes)

    if re_header['type'] == type and re_header['action'] == action:
        re_data_len = re_header['len']
        re_data_bytes = conn.recv(re_data_len)
        re_data = struct_tcp.decode_header_bytes_or_data_bytes(re_data_bytes)
        return re_data
    return False

def schedule(x,y):
    #进度条
    dd=int(y/x*100)
    str1='*'*dd
    str2='\r[%-100s]'%str1
    print(str2+str(dd)+'%',end=' ')