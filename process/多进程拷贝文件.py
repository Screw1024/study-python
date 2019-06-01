from multiprocessing import Pool,Manager
import os

def copyFile(name,oldFolderName,newFolderName,queue):
    fr = open(oldFolderName+"/"+name)
    fw = open(newFolderName+"/"+name,"w")

    content = fr.read()
    fw.write(content)
    
    fr.close()
    fw.close()

    queue.put(name)

# 类似其他语言的入口函数，增强可读性 
def main():

    #用户输入当前目录下需要拷贝的文件夹名
    oldFolderName = input("请输入需要拷贝的文件夹的名字：")

    #创建新文件夹
    newFolderName = oldFolderName + "副本"
    os.mkdir(newFolderName)

    #获取old文件夹中所有的文件名字 
    fileNames = os.listdir(oldFolderName)

    #多线程拷贝文件
    pool = Pool(5)
    queue = Manager().Queue()

    for name in fileNames:
        pool.apply_async(copyFile,args=(name,oldFolderName,newFolderName,queue))

    #执行时判断进程，%在输出需要用两个，因为转义字符
    num = 0 
    allFilenum = len(fileNames)
    while num<allFilenum:
        queue.get()
        num += 1
        copyRate = num/allFilenum 
        print("\r进度:%.2f%%"%(copyRate*100),end="")
        # end="表示不换行"

    print("已完成")
    # pool.close()
    # pool.join()

#通过__name__这个内置变量，在程序运行是他的值是__main__
#这样就只能在调用时执行其中代码，代替其他语言的入口函数
#同时__name__在被其他模块引入时，值为当前的包的结构
if __name__ == "__main__":
    main()
