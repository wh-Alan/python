# Author:Alan

from lib import my_agreement
from  lib import  common
import os
from conf import settings
def download(now_dir,name,user,filename,client):
    header_dict = {
        'action': 'download',
    }
    header_dict['name'] = name
    header_dict['filename'] = filename
    header_dict['now_dir'] = now_dir

    header_bytes = my_agreement.MyAgreement.header_bytes(header_dict, 0)

    client.send(header_bytes)

    res1 = client.recv(4)
    header_size = my_agreement.MyAgreement.get_header_size('', res1)[0]
    res2 = client.recv(header_size)
    header = my_agreement.MyAgreement.get_header('', res2)
    if header['action'] == 'download':
        data_size = header['size']
        if header['code']==200:
            file_path=os.path.join(settings.DOWNLOAD_PATH,filename)
            dd_size = 0
            with open(file_path, 'wb') as f:
                while dd_size < data_size:
                    line = client.recv(1024)
                    dd_size += len(line)

                    common.schedule(data_size, dd_size)
                    f.write(line)
                f.flush()
            if common.file_md5(file_path)!=header['md5']:
                return False,'文件不一致',{}
            return  header['status'],header['msg'],{}
        return header['status'], header['msg'], {}
    return False, '下载有误', {}