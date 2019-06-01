from multiprocessing import Process
import time

def test():
    while True:
        print("process创建的进程")
        time.sleep(1)

p = Process(target=test)
p.start()
# 这个跟JAVA很想啊，通过process的start属性来控制程序的开始执行
 
while True:
    print("主进程")
    time.sleep(1)
