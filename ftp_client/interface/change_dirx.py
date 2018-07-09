# Author: Alan
# Author: Alan

# Author: Alan

# Author:Alan

from lib import my_agreement
import os

def change_dir(now_dir,name,user,path_name,client):
    if path_name=='b':

        if len(now_dir)>1:
            now_dir.pop()
            return True,'切换成功',now_dir
        else:
            return True,'已经是最顶级了',now_dir
    header_dict = {
        'action': 'change_dir',
    }
    header_dict['name'] = name
    header_dict['now_dir'] = now_dir
    header_dict['path_name'] = path_name
    header_bytes=my_agreement.MyAgreement.header_bytes(header_dict,0)

    client.send(header_bytes)


    res1 = client.recv(4)
    header_size = my_agreement.MyAgreement.get_header_size('', res1)[0]
    res2 = client.recv(header_size)
    header = my_agreement.MyAgreement.get_header('',res2)

    if header['action'] == 'change_dir':
        data_size = header['size']
        res = client.recv(data_size)
        res_all = my_agreement.MyAgreement.get_header('',res)
        print(res_all)
        return res_all['status'], res_all['msg'],res_all['data']
    return False, '系统错误',{}