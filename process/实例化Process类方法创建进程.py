from multiprocessing import Process
import time 

class test(Process):
# 实例化Process类
    def run(self):
        while True:
            print("-----数理化的进程------")
            time.sleep(1)

p = test()
p.start()
# 在Process类的实例化对象执行start方法时，自动执行Proces的run方法

while True:
    print("-----主进程------")
    time.sleep(1)
