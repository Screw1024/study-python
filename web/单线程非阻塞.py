from socket import *

serSocket = socket(AF_INET,SOCK_STREAM)

# 重复使用绑定信息，如果服务器意外断开，加上参数1，将不会等待四次挥手
# serSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

# 绑定本机端口
localAddr = ('127.0.0.1',4399)
serSocket.bind(localAddr)

# 将socket默认阻塞变为一个非阻塞的套接字
serSocket.setblocking(False)

# 将socket默认主动转换为被动，并监听50个
serSocket.listen(50)

# 保存所有已经连接的客户端的信息
clientAddrList = []

while True:

    # 非阻塞没有数据就会产生异常 
    try:
        # 等待一个新的客户端的到来（即完成三次握手的客户端）
        # 创建一个新的套接字，另一个变量存放对象的地址
        clientSocket,clientAddr = serSocket.accept()
    except:
        # 这里连不上新的客户端会产生异常，下面接收不到数据，也会产生异常，而因为
        # 处理机制写为pass，所以看不到异常现象
        pass
    else:
        print('-----[%s]已经连接---'%str(clientAddr))
        
        # 将客户端也转化为非阻塞方式
        clientSocket.setblocking(False)
        clientAddrList.append((clientSocket,clientAddr))
        
    # 上面socket设置成为非阻塞的形式，所以上面即使没有新的服务器连接,也不会一直等待
    # 而是执行下面的接收数据的代码，这部分同样不会堵塞，所以又从上到下再次执行
    for clientSocket,clientAddr in clientAddrList:
        try:
            recvData = clientSocket.recv(1024)
        except:
            pass
        else:
            if len(recvData)>0:
                print("%s:%s"%(str(clientAddr),recvData))
            else:
                clientSocket.close()
                clientAddrList.remove((clientSocket,clientAddr))
                print("------[%s] 断开连接------"%str(clientAddr))
