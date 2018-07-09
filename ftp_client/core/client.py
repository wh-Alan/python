# Author: Alan

from  socket import *
client=socket(AF_INET,SOCK_STREAM)
client.connect(('127.0.0.1',8087))



