# Author: Alan

import re
def number_to_upper(num):
    #支持12位数间的转换
    list_1={
        '0': '0',
        '1':'一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九'
    }
    list_2={

        1:'十',
        2:'百',
        3:'千',
        4:'万',
        5:'十',
        6:'百',
        7:'千',
        8:'亿',
        9:'十',
        10:'百',
        11:'千'
     }
    list_num=list(num)
    list_num.reverse()
    for k,v in enumerate(list_num):
        if k==0:
            list_num[k]=list_1[v]
        elif k==4 or k==8:
            list_num[k] = '%s%s' % (list_1[v], list_2[k])
        else:
            if v == '0': continue
            list_num[k]='%s%s'%(list_1[v],list_2[k])
    list_num.reverse()

    str=''.join(list_num)
    if str.find('0000万')>-1:
        str=str.replace('0000万','零')
    str = re.sub('0+','零',str)
    str = re.sub('零+', '零', str)
    str = re.sub('零万', '万', str)
    str = re.sub('零亿', '亿', str)
    if str[-1]=='零':
        return str[:-1]
    return  str

# print(re.findall('\([^[\(\)]+\)',expression))
def count(list,strx):
    #计算一次结果
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


n
def first(str):
    #处理算术运算符第一级别(**)
    list=re.findall('(\([\-]?\d+\.?\d*\)|\d+\.?\d*)(\*\*)(\([\-]?\d+\.?\d*\)|\d+\.?\d*)', str)
    if not list:
        return str
    else:
        str = count(list[0], str)
        return first(str)
def second(str):
    #处理算术运算符第二级别(%//*/)
    list = re.findall('(\([\-]?\d+\.?\d*\)|\d+\.?\d*)(\%|\/\/|\*|\/)(\([\-]?\d+\.?\d*\)|\d+\.?\d*)', str)
    if not list:
        return str
    else:
        str = count(list[0], str)
        return second(str)
def third(str):
    #处理算术运算符第三级别(+-)
    list = re.findall('([\-]?\d+\.?\d*|\([\-]?\d+\.?\d*\))(\+|\-)(\([\-]?\d+\.?\d*\)|\d+\.?\d*)', str)
    if not list:
        return str
    else:
        str = count(list[0], str)
        return third(str)

def bracket(strx):
    #处理括号中的内容
    list=re.findall('\((?:[\-]?\d+\.?\d*|\([\-]?\d+\.?\d*\))(?:(?:\*\*|\/\/|\%|\*|\/|\+|\-)(?:\d+\.?\d*|\([\-]?\d+\.?\d*\))*)+\)', strx)
    if not list:return strx
    else:
        strx1=deal_expression(list[0][1:-1])
        strx=strx.replace(list[0], strx1, 1)
        return bracket(strx)


def deal_expression(strx):
    #处理表达式
    rank_sym_pattern=[

    ]
    strx=first(strx)
    strx=second(strx)
    strx=third(strx)
    return strx
# expression='22//2+1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-((-4)*3)/(16-3*2))'
# print(deal_expression(bracket(expression)))
# while True:
#     ex=input('ex>>>:').strip()
#     if not ex:continue
#     if ex=='q':break
#     print(deal_expression(bracket(ex)).strip('()'))

with open('b.xml','r',encoding='utf-8') as f:
    xml_text=f.read()
print(xml_text)
