# Author: Alan
import os

BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


HOST_INI_PATH=os.path.join(BASE_PATH,'conf','host_configparser.ini')

CMD_LOG_PATH=os.path.join(BASE_PATH,'log','cmd_log')
