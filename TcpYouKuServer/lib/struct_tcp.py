# Author: Alan
import struct
import json,pickle

#自定义协议

def pack_header(header_dict,data):
    #处理tcp发送数据
    data_bytes=pickle.dumps(data)

    header_dict['len']=len(data_bytes)
    header_bytes=pickle.dumps(header_dict)

    header_len=len(header_bytes)
    header_len_bytes=struct.pack('i',header_len)
    return   header_len_bytes+header_bytes+data_bytes
def unpack_header_len(header_len_bytes):
    #解析pack的数字
    return struct.unpack('i',header_len_bytes)[0]

def decode_header_bytes_or_data_bytes(x_bytes):
    #反解数据
    return pickle.loads(x_bytes)