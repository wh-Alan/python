# Author: Alan
import os
BATH_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

'''
文件存数据配置
'''
DB_admin_path=os.path.join(BATH_PATH,'db','admin')
DB_user_path=os.path.join(BATH_PATH,'db','user')
DB_dwn_records_path=os.path.join(BATH_PATH,'db','dwn_records')
DB_video_path=os.path.join(BATH_PATH,'db','video')
DB_notice_path=os.path.join(BATH_PATH,'db','notice')

'''
数据库配置
'''

DB_host='localhost'
DB_port=3306
DB_user='root'
DB_password=''
DB_db='youku'

Videos_path=os.path.join(BATH_PATH,'videos')
