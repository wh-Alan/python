# Author:Alan

from lib import my_agreement
import os
from  lib import  common
def upload(now_dir,name,user,path,client):
    header_dict = {
        'action': 'upload',
    }
    if not os.path.isfile(path):
        return False,'这不是一个文件的路径',{}

    filename=os.path.basename(path)
    filesize=os.path.getsize(path)
    if (filesize+user['user']['mydir_size'])>=user['user']['max_size']:
        return False,'文件过大，上传空间不够了',{}
    header_dict['name']=name
    header_dict['filename']=filename
    header_dict['now_dir']=now_dir
    header_dict['md5']=common.file_md5(path)

    header_bytes=my_agreement.MyAgreement.header_bytes(header_dict,filesize)

    client.send(header_bytes)

    line_0=0
    with open(path,'rb') as f:
        for line in f:
            client.send(line)
            line_0+=len(line)
            common.schedule(filesize,line_0)
    res1 = client.recv(4)
    header_size = my_agreement.MyAgreement.get_header_size('', res1)[0]
    res2 = client.recv(header_size)
    header = my_agreement.MyAgreement.get_header('',res2)
    if header['action'] == 'upload':
        data_size = header['size']
        res = client.recv(data_size)
        res_all = my_agreement.MyAgreement.get_header('',res)
        print(res_all)
        return res_all['status'], res_all['msg'],{}
    return False, '上传有误',{}