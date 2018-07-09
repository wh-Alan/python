# Author: Alan
import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

from lib.common import get_path
import os
def mk_dir(obj,header):
    path = get_path(DB_PATH, header['now_dir'])
    file_path = os.path.join(path, header['dirname'])
    header_dict = {
        'action': 'mk_dir',
        'size': 0
    }
    if os.path.exists(file_path):
        re_data={
            'code':500,
            'status':False,
            'msg':'目录已存在'
        }
    else:
        re_data = {
            'code': 200,
            'status': True,
            'msg': '创建成功'
        }
        os.mkdir(file_path)
    obj_deal = my_agreement.MyAgreement(header_dict, re_data)
    re_res = obj_deal.deal_data()
    obj.request.send(re_res)