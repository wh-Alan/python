# Author: Alan
import time,random
from conf.settings import ATM_BREAK_RECORDS_PATH,ATM_OPERATION_PATH,ATM_USER_CONSUMER_PATH,\
    ATM_USER_PATH,MAX_CREDIT_LIMIT,MIN_CREDIT_LIMIT
from lib.common import find_file_max_id,insert_a_file,name_exist,update_w_file,get_file_line_info


class atm:
    user = ''#卡号
    user_name=''#用户名
    user_info=[]
    dict_list = []
    def __init__(self):
        operation = [
            ['申请信用卡或是注册账户',self.register],
            ['登录',self.login],
            ['取钱',self.withdraw],
            ['存钱',self.deposit],
            ['还款',self.repay],
            ['转账',self.transfer],
            ['操作记录',self.operate],
            ['账单',self.bill],
            ['消费流水',self.run_water],
            ['修改密码',self.update_pwd],
            ['冻结账户',self.freez_account],
            ['解冻账户',self.not_freez_account],
            ['退出登录',self.logout],
        ]
        self.dict_list = operation

    def auth(func):
        #登录装饰器
        def wrapper(self, *args, **kwargs):
            if not self.user:
                print('请登录!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                return  self.login()
            return func(self, *args, **kwargs)

        return wrapper
    def register(self):
        #注册
        #格式：卡号，name,pwd,余额，欠款多少，是否冻结，上次登录时间
        id=find_file_max_id(ATM_USER_PATH)
        print('给你分配的卡号为：%s,请牢记或保存好它' % id)
        while True:
            name=input('请设置信用卡用户名：').strip()
            if not name:continue
            if name=='q':return  True
            # 注册时检测用户名是否唯一
            if name_exist(ATM_USER_PATH, name, 1):
                print('用户名已存在！')
                continue
            break
        while True:
            pwd = input('请设置信用卡密码：').strip()
            if not pwd: continue
            if pwd == 'q':return True
            break
        #随机分配额度
        limit=self.limit_random()
        local_time=time.strftime('%Y-%m-%d %H:%M:%S')
        print('你当前的信用卡额度为%s'%limit)
        content='%s,%s,%s,%s,%s,0,%s\n'%(id,name,pwd,limit,limit,local_time)

        if insert_a_file(ATM_USER_PATH,content):
            #写入操作日志
            insert_a_file(ATM_OPERATION_PATH,'ATM,用户：%s 卡号：%s注册成功 %s'%(id,name,local_time))
            return True
        print('注册出错')
        return False
    def login(self):
        #登录
        if self.user:
            print('用户%s已登录'%self.user_name)
            return True
        while True:
            id = input('请输入卡号：').strip()
            if id == 'q':return True
            if not id:continue
            pwd = input('请输入密码：').strip()
            if pwd == 'q':return True
            if not pwd: continue
            with open(ATM_USER_PATH, 'r', encoding='utf-8') as f:
                for lines in f:
                    line_list=lines.strip(' \n').split(',')
                    if line_list[0]==id and line_list[2]==pwd:
                        if line_list[5]=='1':
                            print('该账户已被冻结')
                            continue
                        else:
                            local_time=time.strftime('%Y-%m-%d %H:%M:%S')
                            line_list[6]=local_time
                            self.user = line_list[0]
                            self.user_name = line_list[1]
                            self.user_info=line_list
                            print('登录成功')
                            break

                else:
                    print('卡号或密码错误')
                    continue
            # 修改登录时间
            update_w_file(ATM_USER_PATH, '%s\n' % (','.join(self.user_info)), self.user)
            insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s登录成功 %s\n' % (self.user_name, self.user, local_time))
            return False

    @auth
    def withdraw(self):
        #取钱
        user_info=self.user_info
        print('%s用户你好！你的余额为：%s,当前欠款为：%s'%(self.user_name,user_info[3],user_info[4]))
        while True:
            p=input('请输入你要取走的金额(5%的手续费)：').strip()
            if p=='q':return True
            if not p.isdigit():continue
            p=int(p)
            num_balance=float(user_info[3])
            if p*1.05>num_balance:
                print('余额不足！')
                continue
            break
        local_time = time.strftime('%Y-%m-%d %H:%M:%S')
        num_balance-=p*1.05
        user_info[3]=str(num_balance)
        self.user_info=user_info
        update_w_file(ATM_USER_PATH, '%s\n' % (','.join(self.user_info)), self.user)
        insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s取款%s于%s（手续费%s）\n' %
                      (self.user_name, self.user, p,local_time,p*0.05))
        insert_a_file(ATM_USER_CONSUMER_PATH, '%s,%s,取款,%s,%s\n' % (local_time,self.user, 0-p, 0-p*0.05))

        print('取款成功！当前余额为：%s'%num_balance)
        print('请继续你的操作！')
        return False

    @auth
    def deposit(self):
        # 存钱
        user_info = self.user_info
        print('%s用户你好！你的余额为：%s,当前欠款为：%s' % (self.user_name, user_info[3], user_info[4]))
        while True:
            p = input('请输入你要存入的金额：').strip()
            if p == 'q': return True
            if not p.isdigit(): continue
            p = int(p)
            if p <= 0:
                print('金额够小！')
                continue
            break
        local_time = time.strftime('%Y-%m-%d %H:%M:%S')
        num_balance=float(user_info[3])
        num_balance+=p
        user_info[3] = str(num_balance)
        self.user_info = user_info
        update_w_file(ATM_USER_PATH, '%s\n' % (','.join(self.user_info)), self.user)
        insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s存款%s于%s（手续费%s）\n' %
                      (self.user_name, self.user, p, local_time, p * 0.05))
        insert_a_file(ATM_USER_CONSUMER_PATH, '%s,%s,存款,%s,%s\n' % (local_time, self.user,  p, 0))

        print('存款成功！当前余额为：%s' % num_balance)
        print('请继续你的操作！')
        print()
        return False

    @auth
    def repay(self):
        # 还款
        user_info = self.user_info
        if float(user_info[4])==0:
            print('当前欠款为0，无需还款！')
            print()
            return True
        print('%s用户你好！你的余额为：%s,当前欠款为：%s' % (self.user_name, user_info[3], user_info[4]))
        while True:
            p = input('请输入你要还款的金额（从当前余额扣款）：').strip()
            if p == 'q': return True
            if not p.isdigit(): continue
            p = int(p)
            num_balance = float(user_info[3])
            num_debt = float(user_info[4])
            if p <= 0:
                print('金额够小！')
                continue
            if p > num_balance:
                print('超过余额限制')
                continue
            break
        if p > num_debt:
            p = num_debt
        local_time = time.strftime('%Y-%m-%d %H:%M:%S')
        num_balance -= p
        num_debt -= p
        user_info[3]=str(num_balance)
        user_info[4]=str(num_debt)
        self.user_info=user_info
        update_w_file(ATM_USER_PATH, '%s\n' % (','.join(self.user_info)), self.user)
        insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s还款%s于%s\n' %
                      (self.user_name, self.user, p, local_time))
        insert_a_file(ATM_USER_CONSUMER_PATH, '%s,%s,还款,%s,%s\n' % (local_time, self.user, 0-p, 0))
        if num_debt == 0:
            print('已成功还请欠款！当前余额为：%s' % num_balance)
            return True
        print('还款成功！当前余额为：%s,欠款为：%s' % (num_balance, num_debt))
        return False

    @auth
    def transfer(self):
        # 转账
        user_info = self.user_info
        print('%s用户你好！你的余额为：%s,当前欠款为：%s' % (self.user_name, user_info[3], user_info[4]))

        while True:
            name_x=input('请输入你要转账的账户的卡号：').strip()
            if name_x=='q':return True
            if not name_x.isdigit() or  name_x==self.user or  not name_exist(ATM_USER_PATH,name_x,0) :
                print('卡号不存在或有误')
                continue
            user_info1=get_file_line_info(ATM_USER_PATH,name_x,0)
            break
        while True:
            p = input('请输入你要转账的金额（从当前余额扣款）：').strip()
            if p == 'q': return True
            if not p.isdigit(): continue
            p = int(p)
            num_balance = float(user_info[3])
            num_balance1 = float(user_info1[3])
            if p <= 0:
                print('金额够小！')
                continue
            if p > num_balance:
                print('超过余额限制')
                continue
            break
        num_balance -= p
        num_balance1 += p
        user_info[3]=str(num_balance)
        user_info1[3]=str(num_balance1)
        self.user_info=user_info

        local_time = time.strftime('%Y-%m-%d %H:%M:%S')
        update_w_file(ATM_USER_PATH, '%s\n' % (','.join(self.user_info)), self.user)
        update_w_file(ATM_USER_PATH, '%s\n' % (','.join(user_info1)), name_x)
        insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s向卡号%s转账%s于%s\n' %
                      (self.user_name, self.user, name_x,p, local_time))
        insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s收到卡号%s的转账%s于%s\n' %
                      (user_info1[1], name_x, self.user, p, local_time))
        insert_a_file(ATM_USER_CONSUMER_PATH, '%s,%s,向%s转账,%s,%s\n' % (local_time, self.user,name_x, 0 - p, 0))
        insert_a_file(ATM_USER_CONSUMER_PATH, '%s,%s,收到%s的转账,%s,%s\n' % (local_time, name_x,self.user, p, 0))
        print('转账成功！当前余额为：%s,欠款为：%s' % (num_balance, user_info[4]))
        print()

    @auth
    def operate(self):
        #操作记录
        with open(ATM_OPERATION_PATH,'r',encoding='utf-8') as f:
            str='ATM,用户：%s 卡号：%s'%(self.user_name,self.user)
            for lines in f:
                if lines.find(str)==0:
                    print(lines,end=' ')

        return True

    @auth
    def bill(self):
        #账单
        while True:
            month = input('请输入查看哪一月账单的月份：').strip()
            if month == 'q': return True
            if not month.isdigit() or int(month)>12:
                print('输入有误')
                continue
            break
        local_year = time.strftime('%Y-')
        re_date="%s%s"%(local_year,month if int(month)>9 else month.zfill(2))
        earning=0#收入
        expend=0#支出
        with open(ATM_USER_CONSUMER_PATH,'r',encoding='utf-8') as f:
            for lines in f:
                line_list=lines.strip(' \n').split(',')
                if line_list[0].find(re_date)>-1 and line_list[1]==self.user:
                    if float(line_list[3])>0:
                        earning+=float(line_list[3])
                    else:
                        expend += 0-(float(line_list[3]))
        print('%s月份的收入为：%s，支出为：%s'%(month,earning,expend))
        print()
        return True

    @auth
    def run_water(self):
        #消费流水
        while True:
            month = input('请输入查看哪一月消费流水的月份：').strip()
            if month == 'q': return True
            if not month.isdigit() or int(month) > 12:
                print('输入有误')
                continue
            break
        local_year = time.strftime('%Y-')
        re_date = "%s%s" % (local_year, month if int(month) > 9 else month.zfill(2))
        with open(ATM_USER_CONSUMER_PATH, 'r', encoding='utf-8') as f:
            print('日期','用户','具体情况','涉及金额','手续费')
            for lines in f:
                line_list = lines.strip(' \n').split(',')
                if line_list[0].find(re_date) > -1 and line_list[1] == self.user:
                    for i in line_list:
                        print(i,end=' ')
                    print()
        print()
        return True
    def freez_account(self):
        while True:
            id = input('请输入要冻结卡号：').strip()
            if id == 'q': return True
            if not id: continue
            pwd = input('请输入密码：').strip()
            if  pwd == 'q': return True
            if not pwd: continue
            with open(ATM_USER_PATH, 'r', encoding='utf-8') as f:
                for lines in f:
                    line_list=lines.strip(' \n').split(',')
                    if line_list[0]==id and line_list[2]==pwd:
                        if line_list[5]=='1':
                            print('该账户已被冻结')
                            continue
                        else:
                            local_time=time.strftime('%Y-%m-%d %H:%M:%S')
                            line_list[5]='1'
                            break

                else:
                    print('卡号或密码错误')
                    continue
            # 修改登录时间

            update_w_file(ATM_USER_PATH, '%s\n' % (','.join(line_list)), id)
            insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s冻结自身账户 %s\n' % (line_list[1], id, local_time))
            if self.user==id:
                self.user=''
                self.user_name=''
                self.user_info=[]
            print('卡号%s冻结成功！' % id)
            print()
            return True
    def not_freez_account(self):
        while True:
            id = input('请输入要解冻卡号：').strip()
            if id == 'q': return True
            if not id: continue
            pwd = input('请输入密码：').strip()
            if  pwd == 'q': return True
            if not pwd: continue
            with open(ATM_USER_PATH, 'r', encoding='utf-8') as f:
                for lines in f:
                    line_list=lines.strip(' \n').split(',')
                    if line_list[0]==id and line_list[2]==pwd:
                        if line_list[5]=='0':
                            print('该账户未被冻结')
                            continue
                        else:
                            local_time=time.strftime('%Y-%m-%d %H:%M:%S')
                            line_list[5]='0'
                            break

                else:
                    print('卡号或密码错误')
                    continue
            # 修改登录时间

            update_w_file(ATM_USER_PATH, '%s\n' % (','.join(line_list)), id)
            insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s解冻自身账户 %s\n' % (line_list[1], id, local_time))
            print('解冻成功')
            print()
            return True

    @auth
    def logout(self):
        self.user = ''
        self.user_name = ''
        self.user_info = []
        print('退出登录成功')
        print()
        return True

    @auth
    def update_pwd(self):
        #修改密码
        while True:
            pwd = input('请设置新密码：').strip()
            if not pwd: continue
            if pwd == 'q':return True
            break
        self.user_info[2]=pwd
        local_time = time.strftime('%Y-%m-%d %H:%M:%S')
        update_w_file(ATM_USER_PATH, '%s\n' % (','.join(self.user_info)), self.user)
        insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s修改密码 %s\n' % (self.user_name, self.user, local_time))
        return True
    def limit_random(self):
        ##随机分配额度
        num=int(random.randint(MIN_CREDIT_LIMIT, MAX_CREDIT_LIMIT)/1000)
        return  float(num*1000)


    def pay_interfance(self,all_price, log_str,cart_user):
        while True:
            id = input('请输入卡号：').strip()
            if id == 'q':return True
            if not id:continue
            pwd = input('请输入密码：').strip()
            if pwd == 'q':return True
            if not pwd: continue
            with open(ATM_USER_PATH, 'r', encoding='utf-8') as f:
                for lines in f:
                    line_list=lines.strip(' \n').split(',')
                    if line_list[0]==id and line_list[2]==pwd:
                        if line_list[5]=='1':
                            print('该账户已被冻结')
                            continue
                        else:
                            local_time=time.strftime('%Y-%m-%d %H:%M:%S')
                            break

                else:
                    print('卡号或密码错误')
                    continue
            # 修改
            if all_price>float(line_list[3]):
                print('余额不足')
                return  False
            line_list[3]=str(float(line_list[3])-all_price)
            update_w_file(ATM_USER_PATH, '%s\n' % (','.join(line_list)), line_list[0])
            insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s商城付款%s于 %s\n' % (line_list[1],
                                                               line_list[0], all_price,local_time))
            insert_a_file(ATM_USER_CONSUMER_PATH, '%s,%s,商城付款,%s,%s\n' % (local_time, line_list[0], 0 - all_price,0))
            return True

    def register_interfance(self):
        def register(self):
            # 注册
            # 格式：卡号，name,pwd,余额，欠款多少，是否冻结，上次登录时间
            id = find_file_max_id(ATM_USER_PATH)
            print('给你分配的卡号为：%s,请牢记或保存好它' % id)
            while True:
                name = input('请设置信用卡用户名：').strip()
                if not name: continue
                if name == 'q': return False
                # 注册时检测用户名是否唯一
                if name_exist(ATM_USER_PATH, name, 1):
                    print('用户名已存在！')
                    continue
                break
            while True:
                pwd = input('请设置信用卡密码：').strip()
                if not pwd: continue
                if pwd == 'q': return False
                break
            # 随机分配额度
            limit = self.limit_random()
            local_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print('你当前的信用卡额度为%s' % limit)
            content = '%s,%s,%s,%s,%s,0,%s\n' % (id, name, pwd, limit, limit, local_time)

            if insert_a_file(ATM_USER_PATH, content):
                # 写入操作日志
                insert_a_file(ATM_OPERATION_PATH, 'ATM,用户：%s 卡号：%s注册成功 %s' % (id, name, local_time))
                return True
            print('注册出错')
            return False

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

if __name__ =='__main__':
    atm_init()