# Author: Alan
import os,sys
import socketserver
import struct
import json
BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_PATH)

from interface.register import register
from interface.login import login
from interface.change_dir import change_dir
from interface.upload import upload
from interface.download import download
from interface.check_file import check_file
from interface.mk_dir import mk_dir
from interface.remove_dir import remove_dir

# from conf.settings import DB_USER
# from lib import common
# common.save_file_pickle(DB_USER,{})

#print(os.path.getsize(r'D:\ftp_server\db\alex\junqi2018_5_23_23_19.jgs'))
action_list={
            'register':register,
            'login':login,
            'change_dir':change_dir,
            'upload':upload,
            'download':download,
            'check_file':check_file,
            'mk_dir':mk_dir,


}



# 通信循环
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(4)
                if not data: break
                header_size=struct.unpack('i',data)[0]
                header_json=self.request.recv(header_size).decode('utf-8')
                header=json.loads(header_json)
                action_list[header['action']](self,header)
            except ConnectionResetError:
                break
        self.request.close()


if __name__ == '__main__':
    # 连接循环
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8087), MyTCPHandler)
    server.serve_forever()