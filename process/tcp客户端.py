from socket import *

connNum = raw_input("请输入要连接的服务器次数：")

for i in range(int(connNum)):
    s = socket(AF_INET,SOCK_STREAM)
    s.connect(("127.0.0.1",4399))
    print(i)
