# Author: Alan
import os
#项目路径
BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#项目日志路径
LOG_PATH=os.path.join(BASE_PATH,'log','access.log')

#商城
MALL_GOODS_PATH=os.path.join(BASE_PATH,'db','mall_goods')
MALL_USER_PATH=os.path.join(BASE_PATH,'db','mall_user')

#ATM信用卡
ATM_USER_PATH=os.path.join(BASE_PATH,'db','ATM_user')
ATM_OPERATION_PATH=os.path.join(BASE_PATH,'db','ATM_operation')#操作记录
ATM_BREAK_RECORDS_PATH=os.path.join(BASE_PATH,'db','ATM_break_records')#违约记录
ATM_USER_CONSUMER_PATH=os.path.join(BASE_PATH,'db','ATM_user_consumer')#账单

#信用卡额度范围
MAX_CREDIT_LIMIT=50000
MIN_CREDIT_LIMIT=10000

# print(BASE_PATH,MALL_USER_PATH)
