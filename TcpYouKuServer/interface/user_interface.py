# Author: Alan
from lib import struct_tcp,common
from conf import settings
import os,hashlib,json,struct,pymysql,pickle
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
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    cursor.execute('''select id from `user` where `phone`=%s''', data['phone'])
    user_info = cursor.fetchone()

    re_header = {
        'type': 'user',
        'action': 'register',
    }

    if user_info:
        re_data = {
            'status': False,
            'msg': '用户名已存在'

        }
    else:

        try:
            res_db = cursor.execute('''insert into `user`(`phone`,pwd,money,is_member,is_delete) values(%s,%s,%s,%s,%s)''',
                                    (data['phone'],data['pwd'],0,0,0))
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
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)


def login(header,conn):
    #print('------------登录----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    cursor.execute('''select id,is_delete,money,is_member from `user` where `phone`=%s and pwd=%s''', (data['phone'],data['pwd']))
    user_info = cursor.fetchone()

    re_header = {
        'type': 'user',
        'action': 'login',
    }
    if user_info:

        if user_info[1]==1:
            re_data = {
                'status': False,
                'msg': '账户已被锁定'
            }
        else:
            re_data = {
                'status': True,
                'msg': '登录成功',
                'data':user_info
            }
    else:
        re_data = {
            'status': False,
            'msg': '用户名或密码错误'
        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)
def become_member(header,conn):
    #print('------------冲会员----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)

    cursor.execute('''select id,is_delete,money,is_member from `user` where `phone`=%s''', data['phone'])
    user_info = list(cursor.fetchone())
    re_header = {
        'type': 'user',
        'action': 'become_member',
    }
    user_info[2]+=data['money']
    if user_info[3]==0:
        if user_info[2]>=50:
            user_info[2]-=50
            user_info[3]=1
            re_data={
                'status':True,
                'msg':'冲会员成功',
                'money':user_info,
            }
        else:
            re_data = {
                'status': True,
                'msg': '充值成功，余额咋不足开启会员',
                'money': user_info,
            }

    else:
        re_data = {
            'status': True,
            'msg': '充值成功',
            'money': user_info,
        }
    try:
        cursor.execute('''update `user` set money=%s,is_member=%s where phone=%s''',
                                (user_info[2], user_info[3], data['phone']))
        db_conn.commit()
    except Exception as e:
        print(e)

    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

def dwn_video(header,conn):
    #print('------------下载视频----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    re_header = {
        'type': 'user',
        'action': 'dwn_video',
    }
    cursor.execute('''select url,is_charge,cost,member_cost from `video` where `id`=%s''', data['id'])
    video_list = cursor.fetchone()
    file_path=video_list[0]
    file_size = os.path.getsize(file_path)
    re_header['filesize'] = file_size
    file_pathx, filename = os.path.split(file_path)
    re_header['filename'] = filename
    file_size = os.path.getsize(file_path)
    md5_obj = hashlib.md5()
    md5_obj.update(str(file_size).encode('utf-8'))
    re_header['md5'] = md5_obj.hexdigest()
    cursor.execute('''select id,is_delete,money,is_member from `user` where `phone`=%s''', data['phone'])
    user_info = list(cursor.fetchone())

    if user_info[3] == 1:
        cost = video_list[3]
    else:
        cost = video_list[2]
    if video_list[1] == 0:
        cost = 0
    user_info[2] -= cost
    if user_info[2] < 0:
        conn.send('0'.encode('utf-8'))
        return False
    else:
        conn.send('1'.encode('utf-8'))

    header_bytes = pickle.dumps(re_header)

    header_len = len(header_bytes)
    header_len_bytes = struct.pack('i', header_len)
    conn.send(header_len_bytes)
    conn.send(header_bytes)

    with open(file_path, 'rb') as f:
        for line in f:
            conn.send(line)


    try:
        cursor.execute('''insert into dwn_records(user_id,video_id,cost) values(%s,%s,%s)''',
                                (user_info[0], data['id'], video_list[2]))
        db_conn.commit()
        cursor.execute('''update `user` set money=%s where phone=%s''',
                       (user_info[2], data['phone']))
        db_conn.commit()
    except Exception as e:
        print(e)

def check_dwn_records(header,conn):
    #print('------------查看观影（下载）记录----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)


    re_header = {
        'type': 'user',
        'action': 'check_dwn_records',
    }
    cursor.execute('''select a.video_id,a.cost,c.url from `dwn_records` as a right join `user` as b on a.user_id=b.id and b.phone=%s
                      left join video as c on c.id=a.video_id
                 ''', data['phone'])
    dwn_records_info = cursor.fetchall()
    if dwn_records_info:
        re_data = {
            'status': True,
            'msg': '查询成功',
            'data': dwn_records_info,
            'video':dwn_records_info
        }
    else:
        re_data = {
            'status': True,
            'msg': '暂无记录',
            'data': ()
        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)

def chech_notice(header,conn):
    #print('------------查看公告----------')
    data_len = header['len']
    data_bytes = conn.recv(data_len)
    data = struct_tcp.decode_header_bytes_or_data_bytes(data_bytes)
    re_header = {
        'type': 'user',
        'action': 'chech_notice',
    }
    cursor.execute('''select id,content from notice where is_delete=0''')
    notice_list = cursor.fetchall()

    if not notice_list:
        re_data = {
            'status': True,
            'msg': '暂无公告',
            'data': notice_list

        }
    else:
        re_data = {
            'status': True,
            'msg': '查询成功',
            'data': notice_list

        }
    re_data_bytes = struct_tcp.pack_header(re_header, re_data)
    conn.send(re_data_bytes)


action_dict={
    'register':register,
    'login':login,
    'become_member':become_member,
    'dwn_video':dwn_video,
    'check_dwn_records':check_dwn_records,
    'chech_notice':chech_notice
}