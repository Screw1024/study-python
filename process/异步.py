from multiprocessing import Pool
import time
import os

def test():
    print("---本进程的pid=%d,父进程的pid=%d---"%(os.getpid(),os.getppid()))
    for i in range(3):
        print("***%d***"%i)
        time.sleep(1)
    return "陈永建真帅"

def test2(args):
    print("---callback func---pid=%d"%os.getpid())
    print("---callback func---args=%s"%args)

pool = Pool(3)
pool.apply_async(func=test,callback=test2)

time.sleep(5)

print("---主进程的pid=%d---"%os.getpid())