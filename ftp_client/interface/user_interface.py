# Author: Alan
from core import client
from lib import my_agreement

def register(name,pwd,client):
    header_dict={
        'action': 'register',
    }
    data_dict={
        'name':name,
        'pwd':pwd
    }
    obj=my_agreement.MyAgreement(header_dict,data_dict)

    data=obj.deal_data()
    client.send(data)
    res1=client.recv(4)
    header_size=obj.get_header_size(res1)[0]
    res2=client.client.recv(header_size)
    header=obj.get_header(res2)
    if header['action']=='register':
        data_size=header['size']
        res=client.recv(data_size)
        res_all=obj.get_header(res)
        print(res_all)
