from socket import * 
from time import sleep

# 创建socket
tcpSerSocket = socket(AF_INET,SOCK_STREAM)

#绑定本地信息
address = ('',4399)
tcpSerSocket.bind(address)

connNum = int(raw_input("请输入最大的链接数："))

# scoket创建的套接字是主动的，如果想要改为被动形式，需要将其改变
tcpSerSocket.listen(connNum)

while True:
    # 如果有新的客户端请求连接服务器,将产生一个新的套接字专门为这个客户端服务器
    newSocket,clientAddr = tcpSerSocket.accept()
    print clientAddr
    sleep(1)

