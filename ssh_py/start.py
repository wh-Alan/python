# Author: Alan

import os,sys

base_path=os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

from core import src


if __name__ == '__main__':
    src.run()
