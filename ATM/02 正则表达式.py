import re

# print(re.findall('\w','ab_123 4_c\n\t'))
# print(re.findall('ab','aaaab aab_12a3 4_c\n\t'))

# print(re.findall('\W','ab_123 4_c\n\t'))
# print(re.findall('\s','ab_123  4_c\n\t'))
# print(re.findall('\s\s','ab_1 23  4_c\n\t'))
#                                    \s\s
# print(re.findall('\S\S\S','ab_1 23  4_c\n\t'))
#                                      \S\S\S
# ['ab_','4_c',]

# print(re.findall('\d','a123b_\n\t'))
# print(re.findall('\D','a123 b_\n\t'))

# print(re.findall('^alex','alex my name is alex,alex is sb'))
#                         alex

# print(re.findall('sb$','alex my name is alex_sb,alex is sb'))
#                                                    sb$

# print(re.findall('\n','a123b_\n\t'))
# print(re.findall('\t','a123b_\n\t'))


#：.
# print(re.findall('a.c','123123a1c a2c alexissb aaaaaac a-c a*c'))
#                                                      a.c
# ['a1c','a2c','aac','a-c','a*c']

# .能匹配换行符外的任意字符
# print(re.findall('a.c','123123a1c a2c a\nclexissb aaaaaac a-c a\nc'))
# 让.也能匹配换行符，需添加一个参数
# print(re.findall('a.c','123123a1c a2c a\nclexissb aaaaaac a-c a\nc',re.DOTALL))

# []:匹配的也是一个字符，但这一个字符必须是[]内定义的
# print(re.findall('a[+0-9]c','abc a-c a+c a*c a1c a2c'))
# print(re.findall('a[a-zA-Z]c','aAc abc a-c a+c a*c a1c a2c'))
# print(re.findall('a[\+\-\*\/]c','a12c aAc abc a-c a+c a*c a/c a1c a2c'))
# print(re.findall('a[0-9][0-9]c','a12c aAc abc a-c a+c a*c a/c a1c a2c'))
# print(re.findall('a[0-9]{2}c','a12c aAc abc a-c a+c a*c a/c a1c a2c'))



#重复匹配（不能单独使用）：? * + {m,n}

#？：代表做左侧的字符有0个或者1个,有则必须要匹配，没有也可以将就
# print(re.findall('ab?','a ab abb abbb abbbbbbbb bbbbbba123a',))
# print(re.findall('ab{0,1}','a ab abb abbb abbbbbbbb bbbbbba123a',))

#                                    ab?
# ['a','ab','ab','ab','ab','a','a']

#*: 代表做左侧的字符有0个或者无穷个,有则必须要匹配，没有也可以将就
# print(re.findall('ab*','a ab abb abbb abbbbbbbb bbbbbba123a',))
# print(re.findall('ab{0,}','a ab abb abbb abbbbbbbb bbbbbba123a',))

#+: 代表做左侧的字符有1个或者无穷个,至少取1个，如果有多个则取多个
# print(re.findall('ab+','a ab abb abbb abbbbbbbb bbbbbba123a',))
# print(re.findall('ab{1,}','a ab abb abbb abbbbbbbb bbbbbba123a',))

#{m,n}:代表做左侧的字符有m个到n个,至少取m个，最多取n个,如果不指定n则代表无穷
# print(re.findall('ab{2,4}','a ab abb abbb abbbbbbbb bbbbbba123a',))
#                                                ab{2,4}
# ['abb','abbb','abbbb',]

# print(re.findall('\d+\.?\d*','a12312321312321312321bc123def7gh2.3sf123123.123213a43'))
#                                \d+\.?\d*

#.*与.*?
# print(re.findall('a.*c','a123123123c123123123123c1231231231')) #.*是贪婪匹配
# print(re.findall('a.*?c','a123123123c123123123123c1231231231')) #.*?是非贪婪匹配

# 分组()与|:默认只取组内的结果
# print(re.findall('compan(ies|y)','too many companies is daobi ,the next one is my company'))

#                                                                                 compan(ies|y)
# 把匹配到的内容都取出来，而不是只留组内的结果
# print(re.findall('compan(?:ies|y)','too many companies is daobi ,the next one is my company'))




# print(re.findall('a href="(.*?)"',
#                  '<p>这是https协议</p><a href="https://www.baidu.com"><a href="https://www.python.org">'))
#                                                                      a href="(.*?)"


# print(re.search('e','alex is love love'))
# 从头开始匹配，只要匹配成功一次就结束
# print(re.search('e','alex is love love').group())
# print(re.search('alex','alex is love alex love').group())
# re.match('alex','alex is love alex love')
# re.search('^alex') #与上面的意义一样

# print(re.sub('alex','sb','alex is alex'))

#匹配斜杠
import re


# print(re.findall('a\\\\c','a\c a1c'))  #a\\c
print(re.findall(r'a\\c','a\c a1c'))  #a\\c