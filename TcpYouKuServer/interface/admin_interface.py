# Author: Alan
from lib import struct_tcp,common
from conf import settings
import os,hashlib,pymysql

db_conn = pymysql.connect(
        host=settings.DB_host,
        port=settings.DB_port,
        user=settings.DB_user,
        password=settings.DB_password,
        db=settings.DB_db
    )
cursor = db_conn.cursor()

def register(header,conn):
    #print('------------注册----------')
    data_len=header['len']
    data_bytes=conn.recv(data_len)
    data=struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    cursor.execute('''select id from `admin` where `name`=%s''',data['name'])
    admin_info=cursor.fetchone()
    re_header={
        'type':'admin',
        'action':'register',
    }
    if admin_info:
        re_data = {
            'status':False,
            'msg':'管理员名已存在'
        }
    else:
        try:
            res_db = cursor.execute('''insert into admin(`name`,pwd) values(%s,%s)''', (data['name'],data['pwd']))
            db_conn.commit()
        except Exception as e:
            print(e)
            res_db = False
        if res_db:
            re_data = {
                'status': True,
                'msg': '注册成功'
            }
        else:
            re_data = {
                'status': False,
                'msg': '注册失败'
            }
    re_data_bytes=struct_tcp.pack_header(re_header,re_data)
    conn.send(re_data_bytes)


def login(header,conn):
    # print('------------登录----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    print(data)
    cursor.execute('''select id from `admin` where `name`=%s and pwd=%s''', (data['name'],data['pwd']))
    admin_info = cursor.fetchone()
    re_header = {
        'type': 'admin',
        'action': 'login',
    }
    if admin_info:
        re_data = {
            'status':True,
            'msg':'登录成功'
        }
    else:
        re_data = {
            'status': False,
            'msg': '用户名或密码错误'
        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)
def upload_video(header,conn):
    #print('------------上传视频----------')
    filename = header['filename']
    filesize = header['len']

    video_list=os.listdir(settings.Videos_path)
    re_header = {
        'type': 'admin',
        'action': 'upload_video',
    }
    if filename in video_list:
        re_data = {
            'status': False,
            'msg': '文件已存在'
        }
    else:
        re_data = {
            'status': True,
            'msg': '可上传'
        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

    recv_size = 0
    video_path1=os.path.join(settings.Videos_path,filename)

    with open(video_path1,'wb') as f:
        while recv_size < filesize:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_size += len(recv_data)
        f.flush()
    file_size1 = os.path.getsize(video_path1)
    md5_obj = hashlib.md5()
    md5_obj.update(str(file_size1).encode('utf-8'))
    if header['md5']==md5_obj.hexdigest():
        try:
            res_db = cursor.execute('''insert into video(url,is_charge,cost,member_cost,is_delete) values(%s,%s,%s,%s,%s)''',
                                    (video_path1,header['is_charge'],header['cost'],header['member_cost'],0))
            db_conn.commit()
        except Exception as e:
            print(e)
            res_db = False
        if res_db:
            re_data = {
                'status': True,
                'msg': '上传成功'
            }
        else:
            re_data = {
                'status': False,
                'msg': '上传失败'
            }
    else:
        re_data = {
            'status': False,
            'msg': '文件上传不完整或被篡改'
        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

def get_video_list(header,conn):
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    cursor.execute('''select * from `video`''')
    video_list = cursor.fetchall()
    re_header = {
        'type': 'admin',
        'action': 'get_video_list',
    }
    re_data={
        'data':video_list
    }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

def delete_video(header,conn):
    #print('------------删除视频----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    video_list = common.db_query(settings.DB_video_path)
    video_list[data['id']]['is_delete']=1
    common.db_save(settings.DB_video_path,video_list)
    re_header = {
        'type': 'admin',
        'action': 'delete_video',
    }
    try:
        res_db = cursor.execute(
            '''update video set is_delete=1 where id=%s''',(data['id'],))
        db_conn.commit()
    except Exception as e:
        print(e)
        res_db = False
    if res_db:
        re_data = {
            'status': True,
            'msg': '删除成功'
        }
    else:
        re_data = {
            'status': False,
            'msg': '删除失败'
        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)
def release_notice(header,conn):
    #print('------------发布公告----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    try:
        res_db = cursor.execute(
            '''insert into notice(content,is_delete) values(%s,%s)''',(data['content'],0))
        db_conn.commit()
    except Exception as e:
        print(e)
        res_db = False
    if res_db:
        re_data = {
            'status': True,
            'msg': '发布成功'
        }
    else:
        re_data = {
            'status': False,
            'msg': '发布失败'
        }
    re_header = {
        'type': 'admin',
        'action': 'release_notice',
    }

    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

def chech_capital(header,conn):
    #print('------------查看资金----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)

    cursor.execute('''select sum(cost) as c,(select count(id) from `user` where is_member=1) as d from dwn_records  ''')
    data_list = cursor.fetchone()
    re_header = {
        'type': 'admin',
        'action': 'chech_capital',
    }
    re_data = {
        'data': data_list
    }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)


def check_user(header,conn):
    #print('------------查看用户----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    cursor.execute('''select id,phone,money,is_member,is_delete from `user` ''')
    user_list = cursor.fetchall()


    re_header = {
        'type': 'admin',
        'action': 'check_user',
    }
    re_data = {
        'data': user_list
    }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

def manage_user(header,conn):
    #print('------------管理用户----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    try:
        res_db = cursor.execute('''update `user` set is_delete=%s where phone=%s''', (data['is_lock'], data['phone']))
        db_conn.commit()
    except Exception as e:
        print(e)
        res_db = False
    if res_db:
        re_data = {
            'status': True,
            'msg': '修改成功'
        }
    else:
        re_data = {
            'status': False,
            'msg': '修改失败'
        }
    re_header = {
        'type': 'admin',
        'action': 'manage_user',
    }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)


action_dict={
    'register':register,
    'login':login,
    'upload_video':upload_video,
    'get_video_list':get_video_list,
    'delete_video':delete_video,
    'release_notice':release_notice,
    'chech_capital':chech_capital,
    'check_user':check_user,
    'manage_user':manage_user
}