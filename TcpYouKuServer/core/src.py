# Author: Alan

from threading import Thread
from socket import *
from lib import struct_tcp
from interface import admin_interface,user_interface

def task_tcp(conn):
    try:
        header_len_bytes=conn.recv(4)
        header_len=struct_tcp.unpack_header_len(header_len_bytes)

        header_bytes=conn.recv(header_len)
        header=struct_tcp.decode_header_bytes_or_data_bytes(header_bytes)
        action=header['action']

        if header['type']=='admin':
            admin_interface.action_dict[action](header,conn)
        if header['type']=='user':
            user_interface.action_dict[action](header,conn)
    except ConnectionResetError:
        pass
    finally:
        conn.close()
def run():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('127.0.0.1', 8089))
    s.listen(5)
    while True:
        connx, addr = s.accept()
        print(addr)
        p = Thread(target=task_tcp, args=(connx,))
        p.start()