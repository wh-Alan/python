# Author: Alan
import os,sys
BASE_PATH=os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_PATH)

from  core import src

# from conf import settings
# from lib import common
# common.db_save(settings.DB_video_path,[])
# # common.db_save(settings.DB_user_path,{})
# common.db_save(settings.DB_notice_path,[])
if __name__ == '__main__':
    src.run()


