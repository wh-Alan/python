# Author: Alan
import configparser
import os
def get_filed_ini(path,filed):
    # 取出ini文件中配置项下的信息,返回列表元组对（key=>value）

    config = configparser.ConfigParser()
    config.read(path)
    if not config.has_section(filed):
        return []
    return  config.items(filed)
def save_filed_ini(path,filed,data):
    #修改ini文件中配置项下的信息
    #若有需要请自行改写
    pass

def save_cmd_log(path,str):
    with open(path,'a',encoding='utf-8') as f:
        f.write(str)
        f.flush()
    return os.path.getsize(path)
