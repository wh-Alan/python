# Author: Alan
import json

def db_query(file_path):
    #查询
    with open(file_path,'r') as f:
        res=json.load(f)
    return res

def db_save(file_path,data):
    #修改
    with open(file_path,'w') as f:
        json.dump(data,f)
    return  True

