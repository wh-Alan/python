# Author: Alan
import os,sys

BASE_PATH=os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)


from  core import admin,user
action_list=[
    admin.run,
    user.run
]

if __name__ == '__main__':
    while True:
        print('''
        0:管理员界面
        1:用户界面
        ''')
        res = input('请选择：').strip()
        if res == 'q': break
        if not res: continue
        if res.isdigit() and int(res) < len(action_list):
            res=int(res)
            action_list[res]()
        else:
            print('输入有误')

