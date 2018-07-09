# Author: Alan

# Author:Alan

from lib import my_agreement
import os

def mk_dir(now_dir,name,user,dirname,client):
    header_dict = {
        'action': 'mk_dir',
    }
    header_dict['name'] = name
    header_dict['dirname'] = dirname
    header_dict['now_dir'] = now_dir

    header_bytes=my_agreement.MyAgreement.header_bytes(header_dict,0)

    client.send(header_bytes)


    res1 = client.recv(4)
    header_size = my_agreement.MyAgreement.get_header_size('', res1)[0]
    res2 = client.recv(header_size)
    header = my_agreement.MyAgreement.get_header('',res2)
    if header['action'] == 'mk_dir':
        data_size = header['size']
        res = client.recv(data_size)
        res_all = my_agreement.MyAgreement.get_header('',res)
        print(res_all)
        return res_all['status'], res_all['msg'],{}
    return False, '上传有误',{}