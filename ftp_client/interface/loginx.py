# Author:Alan

from lib import my_agreement
import hashlib
def login(name,pwd,client):
    header_dict={
        'action': 'login',
    }
    m=hashlib.md5()
    m.update(pwd.encode('utf-8'))
    pwd=m.hexdigest()
    data_dict={
        'name':name,
        'pwd':pwd
    }
    obj=my_agreement.MyAgreement(header_dict,data_dict)

    data=obj.deal_data()
    client.send(data)
    res1=client.recv(4)
    header_size=obj.get_header_size(res1)[0]
    res2=client.recv(header_size)
    header=obj.get_header(res2)
    if header['action']=='login':
        data_size=header['size']
        res=client.recv(data_size)
        res_all=obj.get_header(res)
        return res_all['status'],res_all['msg'],res_all
    return False,'登录有误',{}