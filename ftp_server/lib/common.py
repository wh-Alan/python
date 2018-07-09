# Author: Alan
import pickle,os,hashlib
def query_file_pickle(filename):
    #pickle取数据
    with open(filename,'rb') as f:
        res=pickle.load(f)
    return res

def save_file_pickle(filename,data):
    # pickle存数据
    with open(filename,'wb') as f:
        pickle.dump(data,f)
    return True

def get_path(dir_path,now_dir):
    if not now_dir:return dir_path
    dir_path=os.path.join(dir_path,now_dir[0])
    now_dir.pop(0)
    return get_path(dir_path,now_dir)


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