# Author: Alan
from conf import settings
from db import handle_db
import os,pickle

def login_auth(type):
    #带参装饰器认证登录
    def auth_in(func):
        from core import admin
        from core import teacher
        from core import student

        def wrapper(*args,**kwargs):
            if type == 'admin':
                if not admin.login_data['name']:
                    print('请先登录!')
                    if not admin.login():return False
            if type == 'teacher':
                if not teacher.login_data['name']:
                    print('请先登录!')
                    if not teacher.login(): return False

            if type == 'student':
                if not student.login_data['name']:
                    print('请先登录!')
                    if not student.login(): return False
            func(*args,**kwargs)
        return wrapper
    return auth_in

def login_action(name,pwd,type):
    #统一登录方法
    if type=='admin':
        obj=handle_db.Admin.get_obj(name)
        if obj :
            if obj.pwd==pwd:
                return True,'登录成功'
            return False,'密码错误'
        return False,'登录名不存在'
    if type=='teacher':
        obj=handle_db.Teacher.get_obj(name)
        if obj :
            if obj.pwd==pwd:
                return True,'登录成功'
            return False,'密码错误'
        return False,'登录名不存在'
    if type=='student':
        obj=handle_db.Student.get_obj(name)
        if obj :
            if obj.pwd==pwd:
                return True,'登录成功'
            return False,'密码错误'
        return False,'登录名不存在'
def query_obj(class_name,name):
    #以name查询对象，无则返回false
    path= os.path.join(settings.DB_PATH,class_name,name)
    if not os.path.exists(path):
        return False
    with open(path,'rb') as f:
        return pickle.load(f)

def save_obj(obj):
    #保存或修改对象
    path_dir=os.path.join(settings.DB_PATH,obj.__class__.__name__.lower())
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    path=os.path.join(path_dir,obj.name)

    with open(path,'wb') as f:
        pickle.dump(obj,f)
        f.flush()

def list_dir(path):
    if os.path.exists(path):
        return  os.listdir(path)
    return []