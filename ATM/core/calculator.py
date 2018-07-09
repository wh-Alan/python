# Author: Alan
import re
#实现输入数学式子（python里），计算其结果，类似计算器。思路如下：
#1.去括号：先计算最里层括号内的表达式（正则抓出）并计算出值，然后完成替换，最后循环此步骤（递归），直到没有括号或其内无表达式
#2.表达式（没有括号的干扰）计算：按运算符优先级（正则抓出）依次计算出值（递归），然后完成替换，最后会返回一个值（负数则用小括号括起）
#3.支持：python **，%，//等运算，小括号，中括号，及大括号（其实原理是一样的，正则都类似）
#4.坑：替换时如果用re.sub,由于式子包含一些特殊字符需要转义才能替换，然而我用的是replace
#5.输入：如果不是位于表达式的开头的负数请用小括号括起，避免符号混乱
def count_ex(list,strx):
    #计算一次结果 负数用（）括起来
    list_left=re.sub('[\(\)]*','',list[0])
    list_right=re.sub('[\(\)]*','',list[2])
    list_sym=list[1]
    list_str=''.join(list)
    if list_sym=='**':
        num=float(list_left)**float(list_right)
        sym_str=str(num) if num>0 else '(%s)'%num #计算结果
        return strx.replace(list_str,sym_str,1)
    elif list_sym=='//':
        num = float(list_left) // float(list_right)
        sym_str = str(num) if num > 0 else '(%s)' % num  # 计算结果
        return strx.replace(list_str,sym_str,1)
    elif list_sym=='%':
        num = float(list_left) % float(list_right)
        sym_str = str(num) if num > 0 else '(%s)' % num  # 计算结果
        return strx.replace(list_str,sym_str,1)
    elif list_sym=='/':
        num = float(list_left) / float(list_right)
        sym_str = str(num) if num > 0 else '(%s)' % num  # 计算结果
        return strx.replace(list_str,sym_str,1)
    elif list_sym=='*':
        num = float(list_left) * float(list_right)
        sym_str = str(num) if num > 0 else '(%s)' % num  # 计算结果
        return strx.replace(list_str,sym_str,1)
    elif list_sym=='+':
        num = float(list_left) + float(list_right)
        sym_str = str(num) if num > 0 else '(%s)' % num  # 计算结果
        return strx.replace(list_str,sym_str,1)
    elif list_sym=='-':
        num = float(list_left) - float(list_right)
        sym_str = str(num) if num > 0 else '(%s)' % num  # 计算结果
        return strx.replace(list_str,sym_str,1)

def regex_split(str,pattern):
    #处理算术运算符
    list = re.findall(pattern, str)
    if not list:
        return str
    else:
        str = count_ex(list[0], str)
        return regex_split(str,pattern)

def bracket(strx):
    #处理括号中的内容,顺序小括号，中括号，大括号。结束条件没有中括号及大括号和小括号内无表达式（递归）
    regex_bracket=[
        '\((?:[\-]?\d+\.?\d*|\([\-]?\d+\.?\d*\))(?:(?:\*\*|\/\/|\%|\*|\/|\+|\-)(?:\d+\.?\d*|\([\-]?\d+\.?\d*\))*)+\)',
        '\[(?:[\-]?\d+\.?\d*|\([\-]?\d+\.?\d*\))(?:(?:\*\*|\/\/|\%|\*|\/|\+|\-)(?:\d+\.?\d*|\([\-]?\d+\.?\d*\))*)+\]',
        '\{(?:[\-]?\d+\.?\d*|\([\-]?\d+\.?\d*\))(?:(?:\*\*|\/\/|\%|\*|\/|\+|\-)(?:\d+\.?\d*|\([\-]?\d+\.?\d*\))*)+\}'
    ]
    for i in regex_bracket:
        list=re.findall(i, strx)
        if not list:continue
        else:
            strx1=deal_expression(list[0][1:-1])#去掉最外层括号并处理此表达式
            strx=strx.replace(list[0], strx1, 1)#完成替换
            print(list[0],'计算后为',strx1,';则式子化简为：',strx)
    res_end=re.findall(
        '(\{|\[|\((?:[\-]?\d+\.?\d*|\([\-]?\d+\.?\d*\))(?:(?:\*\*|\/\/|\%|\*|\/|\+|\-)(?:\d+\.?\d*|\([\-]?\d+\.?\d*\))*)+\))',
        strx)
    if not res_end:return strx#结束条件
    return bracket(strx)

def deal_expression(strx):
    #处理表达式,运算符优先级，先**,在//,%,/,*,最后+，-
    rank_sym_pattern=[
        '(\([\-]?\d+\.?\d*\)|^\-\d+\.?\d*|\d+\.?\d*)(\*\*)(\([\-]?\d+\.?\d*\)|\d+\.?\d*)',
        '(\([\-]?\d+\.?\d*\)|^\-\d+\.?\d*|\d+\.?\d*)(\%|\/\/|\*|\/)(\([\-]?\d+\.?\d*\)|\d+\.?\d*)',
        '(^\-\d+\.?\d*|\d+\.?\d*|\([\-]?\d+\.?\d*\))(\+|\-)(\([\-]?\d+\.?\d*\)|\d+\.?\d*)'
    ]
    for i in rank_sym_pattern:
        strx=regex_split(strx, i)
    return strx

def run():
    while True:
        ex = input('ex>>>:').strip()
        if not ex: continue
        if ex == 'q': break
        ex=re.sub('\s','',ex)
        print('最后结果为:',deal_expression(bracket(ex)).strip('()'))

# if __name__ == '__main__':
#     run()

# expression='22//2+1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-((-4)*3)/(16-3*2))'
# print(deal_expression(bracket(expression)))

import requests
content='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
<soap:Body>
<GetInfoList xmlns="http://tempuri.org/">
<password>741DF7FFB3174376A4083807901EAFFD</password>
<ctgName>政务要闻</ctgName>
<pageIndex>1</pageIndex>
<pageSize>10</pageSize>
<startTime>2010-02-02</startTime>
<isTop>false</isTop>
</GetInfoList>
</soap:Body>
</soap:Envelope>'''.encode(encoding='utf-8')
headers={
            "Host": "www.shmh.gov.cn",
            "Content-Type":r"text/xml; charset=utf-8",
            "Content-Length":"%s"%(len(content)),
            "SOAPAction":r"http://tempuri.org/GetInfoList"
}
url='http://www.shmh.gov.cn/webservice/MhAppService.asmx'
r = requests.post(url, data=content)
first_html=r.text
print(first_html)
js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))

print ('get js func:\n', js_func)
func_name=re.findall(r'function (\w+)\(', first_html)
print(func_name)
# 提取其中执行JS函数的参数
js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))

print ('get ja arg:\n', js_arg,type(js_arg))
js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
import execjs

def parseCookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]}
ff=execjs.compile(js_func)
cookie_str =ff.call(func_name[0],int(js_arg))
cookie = parseCookie(cookie_str)
print(cookie)

rx = requests.post(url, data=content,headers=headers,cookies=cookie)
with open('b.xml','w',encoding='utf-8') as f:
    f.write(rx.text)
print(rx.text)