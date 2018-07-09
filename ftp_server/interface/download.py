# Author: Alan
import json
from conf.settings import DB_USER,DB_PATH
from  lib import common
from  lib import my_agreement

from lib.common import get_path
import os
def download(obj,header):

    path = get_path(DB_PATH, header['now_dir'])
    file_path = os.path.join(path, header['filename'])
    header_dict = {
        'action': 'download',
        'size':0
    }
    if os.path.exists(file_path):
        header_dict['md5']=common.file_md5(file_path)
        header_dict['code'] = 200
        header_dict['msg'] = '成功下载'
        header_dict['status'] = True
        header_bytes=my_agreement.MyAgreement.header_bytes(header_dict,os.path.getsize(file_path))
        obj.request.send(header_bytes)

        with open(file_path,'rb') as f:
            for line in f:
                obj.request.send(line)

    else:
        header_dict['code']=500
        header_dict['msg']='文件不存在'
        header_dict['status']=False
        header_bytes = my_agreement.MyAgreement.header_bytes(header_dict, 0)
        obj.request.send(header_bytes)