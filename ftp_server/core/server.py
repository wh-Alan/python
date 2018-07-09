# Author: Alan
import socketserver


# 通信循环
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(4)
                if not data: break
                self.request.send('222222'.encode('utf-8'))
            except ConnectionResetError:
                break
        self.request.close()


if __name__ == '__main__':
    # 连接循环
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8088), MyTCPHandler)
    server.serve_forever()