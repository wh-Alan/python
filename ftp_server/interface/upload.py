# Author: Alan

import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

from lib.common import get_path
import os
def upload(obj,header):
    path=get_path(DB_PATH,header['now_dir'])
    file_path=os.path.join(path,header['filename'])

    data_size = header['size']

    dd_size=0
    with open(file_path,'wb') as f:
        while dd_size<data_size:
            line=obj.request.recv(1024)
            dd_size+=len(line)
            f.write(line)
        f.flush()
    header_dict = {
        'action': 'upload'
    }
    md5_x=common.file_md5(file_path)
    if md5_x==header['md5']:
        re_data = {
            'code': 200,
            'status': True,
            'msg': '上传成功',
        }
    else:
        re_data = {
            'code': 500,
            'status': True,
            'msg': '文件不一致',
        }
    obj_deal = my_agreement.MyAgreement(header_dict, re_data)
    re_res = obj_deal.deal_data()
    obj.request.send(re_res)

