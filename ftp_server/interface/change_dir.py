# Author: Alan
import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

from lib.common import get_path
import os
def change_dir(obj,header):
    if header['now_dir']:
        path = get_path(DB_PATH, header['now_dir'])
        file_path = os.path.join(path, header['path_name'])
        header_dict = {
            'action': 'change_dir',
            'size': 0
        }

        if os.path.isdir(file_path):
            header['now_dir'].append(header['path_name'])
            re_data = {
                'code': 200,
                'status': True,
                'msg': '切换成功',
                'data':header['now_dir']
            }
        else:
            re_data = {
                'code': 500,
                'status': False,
                'msg': '这不是一个有效目录',
                'data': header['now_dir']
            }
    else:
        re_data = {
            'code': 500,
            'status': False,
            'msg': '这不是一个有效目录',
            'data': header['now_dir']
        }

    obj_deal = my_agreement.MyAgreement(header_dict, re_data)
    re_res = obj_deal.deal_data()
    obj.request.send(re_res)