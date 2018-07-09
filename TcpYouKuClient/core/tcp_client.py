# Author: Alan

from socket import *
def tcp_conn():
    conn = socket(AF_INET, SOCK_STREAM)
    conn.connect(('127.0.0.1', 8089))
    return conn
