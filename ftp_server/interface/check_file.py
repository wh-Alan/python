# Author: Alan
import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

from lib.common import get_path
import os
def check_file(obj,header):
    if header['now_dir']:
        path = get_path(DB_PATH, header['now_dir'])
        header_dict = {
            'action': 'check_file',
            'size': 0
        }
        if os.path.exists(path):
            dir_list=os.listdir(path)
            re_data = {
                'code': 200,
                'status': True,
                'msg': '当前目录文件如下：',
                'data':dir_list
            }
        else:
            re_data = {
                'code': 500,
                'status': False,
                'msg': '路径不存在',
                'data': []
            }
    else:
        re_data = {
            'code': 500,
            'status': False,
            'msg': '路径不存在',
            'data':[]
        }

    obj_deal = my_agreement.MyAgreement(header_dict, re_data)
    re_res = obj_deal.deal_data()
    obj.request.send(re_res)