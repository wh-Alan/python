# Author: Alan

import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

import os

def login(obj,header):
    data_size=header['size']
    data_json=obj.request.recv(data_size).decode('utf-8')
    data=json.loads(data_json)
    user_info=common.query_file_pickle(DB_USER)
    if not user_info:user_info={}
    header = {
        'action': 'login'
    }


    if data['name']  in user_info and user_info[data['name']]['pwd']==data['pwd']:

        mydir=os.listdir(user_info[data['name']]['mydir'][0])
        re_data = {
            'code': 200,
            'status': True,
            'msg': '登录成功',
            'mydir':mydir,
            'now_dir':[data['name']],
            'user':user_info[data['name']],
        }
    else:
        re_data={
            'code':500,
            'status':False,
            'msg':'用户名或密码错误'
        }
    obj_deal=my_agreement.MyAgreement(header,re_data)
    re_res=obj_deal.deal_data()
    obj.request.send(re_res)