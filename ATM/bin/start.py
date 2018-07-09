# Author: Alan
import os,sys
BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from core.cart import cart
from core.atm import atm
def atm_init():
    # 此处调用atm
    atm_obj = atm()
    while True:
        print('万恶的分割线'.center(50, '-'))
        for index, v in enumerate(atm_obj.dict_list):
            print(index, v[0])
        while True:
            choice = input('请选择你的操作，输入序号即可:').strip()
            if choice == 'q': return True
            if not choice.isdigit() or int(choice) >= len(atm_obj.dict_list):
                print('输入有误')
                continue
            choice = int(choice)
            break
        print(('%s' % atm_obj.dict_list[choice][0]).center(50, '-'))
        res = atm_obj.dict_list[choice][1]()
        while not res:
            res = atm_obj.dict_list[choice][1]()
    return True
def cart_init():
    # 此处调用商城
    cart_obj = cart()
    while True:
        print('邪恶的分割线'.center(50, '-'))
        for index, v in enumerate(cart_obj.operate_func):
            print(index, v[0])
        while True:
            choice = input('请选择你的操作（对应序号即可）：').strip()
            if choice == 'q': return True
            if not choice.isdigit() or int(choice) >= len(cart_obj.operate_func):
                print('输入有误')
                continue
            choice = int(choice)
            break
        print(('%s' % cart_obj.operate_func[choice][0]).center(50, '-'))
        res = cart_obj.operate_func[choice][1]()
        while not res:
            res = cart_obj.operate_func[choice][1]()

    return True
def index():
    place=['银行（ATM）','商城（购物）']
    place_func=[atm_init,cart_init]
    while True:
        print('正义的分割线'.center(50, '-'))
        print('序号','去处')
        for index,v in enumerate(place):
            print(index,v)
        while True:
            choose = input('请选择你的去处（输入序号即可）：').strip()
            if choose=='q':return True
            if choose and choose.isdigit() and int(choose)<len(place):
                choose=int(choose)
                break
            print('请不要乱搞！！！！好好输入。')
        print()
        print(('%s' % place[choose]).center(50, '-'))
        print()
        res = place_func[choose]()
        while not res:
            res = place_func[choose]()
if __name__ =='__main__':
    index()
