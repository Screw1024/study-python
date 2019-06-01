# coding:utf-8

import socket 
import re
from multiprocessing import Process

# 固定值一直都是大写的，在服务器中根目录也是全部大写的
HTML_ROOT_DIR = "./html"


class HTTPServer(object):
    """服务器示例,默认继承object"""
    def __init__(self):
         # AF_INET表示英特网，SOCK_STREAM表示tcp协议
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)


    def start(self):
        # 设置最大链接数
        self.server_socket.listen(10)

        while True:
            client_socket,client_address = self.server_socket.accept()
            # args代表元组，而元组即使只有一个参数，也要用，隔开
            # 客户端的ip地址和端口号都是存放在client_address中，可以通过client_address[0]
            # 和address[1]也可以这样，自动拆箱
            print('[%s:%s]客户端已经连接成功' %client_address)

            handle_client_process = Process(target=self.handle_client,args=(client_socket,))
            handle_client_process.start()
            # 上面hand_client_process已经将客户端资源接收到
            client_socket.close()


    def handle_client(self,client_socket):
        """定义处理客户端的函数"""

        request_data = client_socket.recv(1024)
        print("request data",request_data)
        # splitlines()方法通过换行来分割字符串，并返回列表对象
        request_lines = request_data.splitlines()
        for line in request_lines:
            print(line)

        # GET / HTTP/1.1
        request_start_line = request_lines[0]
        # 通过正则提取响应中的/后的文件名，这个带不带/取决于上面的根目录
        # 请求的是byte格式类型的数据，要转为字符串类型
        file_name = re.match(r"\w+ +(/[^ ]*)",request_start_line.decode("utf-8")).group(1)

        # 将常量写在左边，将变量写在右边，防止少写一个等号
        if "/" == file_name:
            file_name = 'index.html'

        # 读取文件内容，b代表以二进制的方式
        try:
            file = open(HTML_ROOT_DIR + file_name,"rb")
        except IOError:
            response_start_line = "HTTP/1.1 404 Not Found\r\n"
            response_headers = "Server: My server\r\n"
            response_body = "404"
        else:
            file_data = file.read()
            file.close()

            # 构造响应数据
            response_start_line = "HTTP/1.1 200 OK\r\n"
            response_headers = "Server: My server\r\n"
            # 读出来的格式是子节类型，要将其解码
            response_body = file_data.decode("utf-8")

        response = response_start_line + response_headers + "\r\n" + response_body
        print("response data:",response)

        # 响应的报文必须使用改为byte类型，同时编码格式为utf-8
        client_socket.send(bytes(response,"utf-8")) 
        client_socket.close()


    def bind(self,port):
        self.server_socket.bind(("127.0.0.1",port))

def main():
    http_server = HTTPServer()
    http_server.bind(4399)
    http_server.start()
    

if __name__ == '__main__':
    main()
   
