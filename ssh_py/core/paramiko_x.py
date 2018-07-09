# Author: Alan

import paramiko
from lib import  common
from  conf import settings

def execute_cmd(cmd,hostname,port,username,password):
    #执行命令
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=hostname, port=int(port), username=username, password=password)

    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取命令结果
    result = stdout.read()
    res=result.decode('utf-8')
    if not res:
        res=stderr.read().decode('utf-8')
    # 关闭连接

    #记录运行信息
    log_str='%s>>>>>%s\n%s\n'%(hostname,cmd,res)
    common.save_cmd_log(settings.CMD_LOG_PATH,log_str)
    ssh.close()
    print(res)
    return  res

def execute_action(local,remote,hostname,port,username,password,type):
    #执行上传或下载
    conn=paramiko.Transport((hostname,int(port)))
    conn.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(conn)

    log_str='%s上传或下载error'%hostname
    if type=='get':
        sftp.get(remote,r'%s'%local)
        log_str = '%s>>>>>%s-----%s---%s\n' % (hostname, type, remote, local)
    if type=='put':
        sftp.put(r'%s'%local,remote)
        log_str = '%s>>>>>%s-----%s----%s\n' % (hostname, type, local, remote)
    # 记录运行信息

    common.save_cmd_log(settings.CMD_LOG_PATH, log_str)
    conn.close()