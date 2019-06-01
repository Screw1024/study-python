from multiprocessing import Pool
import os
import random
import time

def worker(num):
    for i in range(5):
        print("---pid=%d---num=%d"%(os.getpid(),num))
        time.sleep(1)

pool = Pool(3)

for num in range(10):
    print("---%d---"%num)
    pool.apply_async(worker,(num,))
    # appiy_async()中后一个值需要用元组表示，元组注意如果只有一个元素，必须要加逗号

pool.close()
# 关闭进程池，不能再添加进程进入
pool.join()
# pool创建进程池的方法，不会等待pool的进程全部执行完成之后，再关闭程序，join()等待程序运行完成