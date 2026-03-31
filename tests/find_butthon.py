import sys
import os
import json

import components.adb_utils as adb_utils
# 我需要找到两个按键的位置 所以需要调用adb_utils.tap方法，用不到back
if __name__ == "__main__":
    adb_utils.tap(940,460) 