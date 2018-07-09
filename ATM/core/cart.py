# Author: Alan
from conf.settings import MALL_GOODS_PATH,MALL_USER_PATH
from lib.common import insert_a_file,name_exist
class cart:
    user=''#记录登录状态
    cart_all={}#购物车
    operate_func=[]
    def __init__(self):
        operate_func=[
            ['注册',self.register],
            ['登录', self.login],
            ['购买商品', self.choose_goods],
            ['查看购物车', self.show_cart_list],
            ['结算购物车', self.payfor],
            ['申请信用卡', self.apply_credit_cart],
            ['退出登录', self.logout],
        ]
        self.operate_func=operate_func
    def auth(func):
        # 登录装饰器
        def wrapper(self,*args, **kwargs):
            if not self.user:
                print('请登录!!!!!!!')
                return self.login()
            return func( self,*args, **kwargs)
        return wrapper
    #注册
    def register(self):
        while True:
            name=input('请输入用户名：').strip()
            if not name:continue
            if name=='q':return  True
            # 注册时检测用户名是否唯一
            if name_exist(MALL_USER_PATH,name,0):
                print('用户名已存在！')
                continue
            break
        while True:
            pwd = input('请输入密码：').strip()
            if not pwd: continue
            if pwd == 'q':return True
            break
        if insert_a_file(MALL_USER_PATH,'%s,%s\n'%(name,pwd)):
            print('用户%s注册成功'%name)
            print()
            return True
        print('注册出错')
        print()
        return False
    def login(self):
        if self.user:
            print('不能重复登录!')
            return True
        while True:
            name=input('请输入用户名：').strip()
            if name=='q':return True
            if not name:continue
            break
        while True:
            pwd=input('请输入密码：').strip()
            if pwd=='q':return True
            if not pwd:continue
            break
        with open(MALL_USER_PATH,'r',encoding='utf-8') as f:
            line='%s,%s\n'%(name,pwd)
            for lines in f:
                if line==lines:
                    self.user = name
                    print('登录成功!')
                    print()
                    return True
            print('用户名或密码错误')
            print()
            return False
    @auth
    def choose_goods(self):
        #购买商品
        goods_list={}
        with open(MALL_GOODS_PATH,'r',encoding='utf-8') as f:
            for lines in f:
                lines_list=lines.strip(' \n').split(',')
                goods_list[lines_list[0]]=lines_list
        print('商品列表如下：')
        print('编号', '名称', '单价')
        for i in goods_list:
            for j in goods_list[i]:
                print(j,end=' ')
            print()
        while True:
            input_goods =input('请选择商品（输入对应商品的编号即可,输q退出购买）：').strip()
            if input_goods=='q':return True
            if not input_goods:continue
            if input_goods not in goods_list:
                print('输入有误')
                continue
            break
        while True:
            num=input('请输入购买的商品（%s）的数量：'%goods_list[input_goods][1]).strip()
            if num == 'q': return True
            if not num: continue
            if not num.isdigit() and int(num)>0:
                print('输入错误')
                continue
            num=int(num)
            break
        if input_goods not in self.cart_all:
            cart_x={}
            cart_x['info']=goods_list[input_goods]
            cart_x['name']=goods_list[input_goods][1]
            cart_x['price'] = float(goods_list[input_goods][2])
            cart_x['num'] = num
            self.cart_all[input_goods]=cart_x
        else:
            self.cart_all[input_goods]['num']+=num
        print('添加购物车成功')
        self.show_cart_list()
        print('如需退出当前购买操作，请键入q!')
        return False

    @auth
    def show_cart_list(self):
        #展示当前购物车
        if not self.cart_all:
            print('购物车空空如已！请先去添加')
            print()
            return True
        print('当前购物车信息如下：')
        print('编号', '名称', '单价','数量','单一商品总价')
        all_price=0
        for i in self.cart_all:
            p = self.cart_all[i]['num'] * self.cart_all[i]['price']
            all_price+=p
            print(i,self.cart_all[i]['name'],self.cart_all[i]['price'],self.cart_all[i]['num'],p)
        print('购物车总价为：%s'%all_price)
        print()
        return True

    @auth
    def payfor(self):
        #结算购物车
        from core.atm import atm
        if not self.cart_all:
            print('购物车空空如已！请先去添加')
            return True
        all_price=0
        log_list=[]
        for i in self.cart_all:
            p = self.cart_all[i]['num'] * self.cart_all[i]['price']
            all_price+=p
            log_list.append('%s(%s)'%(self.cart_all[i]['name'],self.cart_all[i]['num']))
        log_str='-'.join(log_list)
        atm_obj = atm()
        if atm_obj.pay_interfance(all_price, log_str, self.user):
            self.cart_all={}
            print('结算成功')
            print()

        return True
    @auth
    def apply_credit_cart(self):
        #申请信用卡
        from core.atm import atm
        atm_obj=atm()
        if atm_obj.register_interfance():
            print('申请成功')
            return True
        print('申请失败')
        print()
        return True

    @auth
    def logout(self):
        #退出登录
        self.user = ''
        self.cart_all={}
        print('退出登录成功')
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
if __name__ =='__main__':
    cart_init()