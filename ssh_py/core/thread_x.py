# Author: Alan

from threading import Thread
def open_thread(func_name,name,data_dict):
    #开一个线程
    p=Thread(target=func_name,name=name,kwargs=data_dict)
    p.start()