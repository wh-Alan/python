# Author: Alan

from interface import ssh_cmd
def run():
    while True:
        cmd=input('请输入命令：').strip()
        if not  cmd: continue
        if cmd=='q':break
        ssh_cmd.deal_cmd(cmd)
        print()
