# Author: Alan

import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

import os

def register(obj,header):
    data_size=header['size']
    data_json=obj.request.recv(data_size).decode('utf-8')
    data=json.loads(data_json)
    user_info=common.query_file_pickle(DB_USER)
    if not user_info:user_info={}

    header = {
        'action': 'register'
    }
    if data['name'] not in user_info:
        path=os.path.join(DB_PATH,data['name'])
        os.mkdir(path)
        user_info[data['name']]={
            'pwd':data['pwd'],
            'mydir':[path],
            'mydir_size':0,
            'max_size':102400000
        }
        common.save_file_pickle(DB_USER,user_info)
        re_data = {
            'code': 200,
            'status': True,
            'msg': '注册成功'
        }
    else:
        re_data={
            'code':500,
            'status':False,
            'msg':'用户名已存在'
        }
    obj_deal=my_agreement.MyAgreement(header,re_data)
    re_res=obj_deal.deal_data()
    obj.request.send(re_res)