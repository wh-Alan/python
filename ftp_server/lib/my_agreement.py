# Author: Alan

import struct
import json
#自定义协议
class MyAgreement:
    size = 4
    def __init__(self,header,data):
        self.data=data
        self.header=header


    def deal_data(self):
        #处理并封装好数据
        data_json = json.dumps(self.data)
        data_bytes = data_json.encode('utf-8')
        self.header['size'] = len(data_bytes)

        header_json = json.dumps(self.header)
        header_bytes = header_json.encode('utf-8')
        header_size = len(header_bytes)

        header_size_bytes = struct.pack('i', header_size)

        return header_size_bytes+header_bytes+data_bytes

    def get_header_size(self,data):
        return struct.unpack('i',data)

    def get_header(self,data):
        return json.loads(data.decode('utf-8'))

    @classmethod
    def header_bytes(cls, header, size):
        header['size'] = size

        header_json = json.dumps(header)
        header_bytes = header_json.encode('utf-8')
        header_size = len(header_bytes)

        header_size_bytes = struct.pack('i', header_size)

        return header_size_bytes + header_bytes