# Author: Alan
# import time
import hashlib,os
def schedule(x,y):
    dd=int(y/x*100)
    str1='*'*dd
    str2='\r[%-100s]'%str1
    print(str2+str(dd)+'%',end=' ')

# for i in range(0,100,3):
#     time.sleep(1)
#     schedule(100,i)

def file_md5(filename):
    #文件一致性
    m=hashlib.md5()
    d_list=[0,2,8,10]
    str2=''
    size=os.path.getsize(filename)
    with open(filename,'rb') as f:
        x=0
        for line in f:
            if x in d_list:
                str2='%s%s'%(str2,line)
            x+=1
    m.update(str2.encode('utf-8'))
    m.update(str(size).encode('utf-8'))
    return m.hexdigest()