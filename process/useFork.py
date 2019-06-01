import os
import time

ret = os.fork()
if ret == 0:
    while True:
        print("你好啊")
        time.sleep(1)
else:
    while True:
        print("李银河")
        time.sleep(1)