'''
******************** 请计算表达式： 1 - 2 * ( (60-30 +(-40.0/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) ) ********************
(-40.0/5) 计算后为 (-8.0) ;则式子化简为： 1-2*((60-30+(-8.0)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))
(9-2*5/3+7/3*99/4*2998+10*568/14) 计算后为 173545.88095238098 ;则式子化简为： 1-2*((60-30+(-8.0)*173545.88095238098)-(-4*3)/(16-3*2))
(60-30+(-8.0)*173545.88095238098) 计算后为 (-1388337.0476190478) ;则式子化简为： 1-2*((-1388337.0476190478)-(-4*3)/(16-3*2))
(-4*3) 计算后为 (-12.0) ;则式子化简为： 1-2*((-1388337.0476190478)-(-12.0)/(16-3*2))
(16-3*2) 计算后为 10.0 ;则式子化简为： 1-2*((-1388337.0476190478)-(-12.0)/10.0)
((-1388337.0476190478)-(-12.0)/10.0) 计算后为 (-1388335.8476190479) ;则式子化简为： 1-2*(-1388335.8476190479)
最后结果为: 2776672.6952380957

'''



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

if __name__ == '__main__':
    run()

# expression='22//2+1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-((-4)*3)/(16-3*2))'
# print(deal_expression(bracket(expression)))