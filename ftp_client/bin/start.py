# Author: Alan
import os,sys

BASE_PATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_PATH)

from core import user

if __name__ == '__main__':
    user.run()