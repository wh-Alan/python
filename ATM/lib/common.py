# Author: Alan
import os
def name_exist(file_path,name,key=0):
    # 判断注册时的用户名是否存在
    with open(file_path, 'r', encoding='utf-8') as f:
        for lines in f:
            line = lines.strip(' \n').split(',')
            if name == line[key]:
                return True
    return False

def get_file_line_info(file_path,id,key=0):
    #得到文件中某一行,返回列表
    with open(file_path,'r',encoding='utf-8') as f:
        for lines in f:
            line = lines.strip(' \n').split(',')
            if id == line[key]:
                return line
        return []

def find_file_max_id(file_path,):
    #找到文件中最大的ID ，注册时自增，主要是ATM注册用，卡号就当ID了。。
    num=1111
    with open(file_path,'r',encoding='utf-8') as f:
        for lines in f:
            num_x=int(lines.strip(' \n').split(',')[0])
            if num<num_x:
                num=num_x
    return num+1

def insert_a_file(file_path,content,model='a'):
    #追加写入文件
    with open(file_path,model,encoding='utf-8') as f:
        f.write(content)
        f.flush()
    return True

def update_w_file(file_path,content,id):
    #修改ATM_user文件
    with open(file_path,'r',encoding='utf-8') as fr, \
            open(r'%s.txt'%file_path, 'w', encoding='utf-8') as f:
        for lines in fr:
            if lines.strip(' \n').split(',')[0]==id:
                f.write(content)
            else:
                f.write(lines)

    os.remove(file_path)
    os.rename(r'%s.txt'%file_path,file_path)
    return True