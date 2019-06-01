# coding:utf-8

import socket 
import re
import sys

from multiprocessing import Process

# 固定值一直都是大写的，在服务器中根目录也是全部大写的
HTML_ROOT_DIR = "./html"
WSGI_PYTHON_DIR = "./wsgi_py_file"


class HTTPServer(object):
    """服务器示例,默认继承object"""
    def __init__(self,application):
        """application指的是框架内的app"""
         # AF_INET表示英特网，SOCK_STREAM表示tcp协议
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        self.app = application


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


    def start_response(self,status,headers):
        # 服务器的响应，列表里面是元组,调用时就获取到了动态文件的status和header
        # 这是请求的py文件中定义的函数，被调用，这也就是WSGI的精华所在
        response_headers = "HTTP/1.1" + status + "\r\n"
        for header in headers:
            response_headers += "%s:%s\r\n" %header
        self.response_headers = response_headers 


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
      
        env = {
            "PATH_INFO": file_name,
            "METHOD": "methon"
        }
        response_body = self.app(env,self.start_response)

        response = self.response_headers + "\r\n" + response_body

        # 响应的报文必须使用改为byte类型，同时编码格式为utf-8
        client_socket.send(bytes(response,"utf-8")) 
        client_socket.close()


    def bind(self,port):
        self.server_socket.bind(("127.0.0.1",port))


def main():
    # 将文件py文件添加到路径中,才能使用__import__魔法糖
    # 单独的文件充当python中的入口函数
    sys.path.insert(1,WSGI_PYTHON_DIR)
    
    # python3 test_server.py web小练习:app
    # sys.argv[]获取启动命令行中的参数，从0开始

    if len(sys.argv) < 2:
        sys.exit("python3 test_server.py web小练习框架:app")
    module_name,app_name = sys.argv[1].split(":")
    # module_name = web小练习
    # app_name = app
    m = __import__(module_name)

    # getattr()返回对象中属性对象
    app = getattr(m,app_name)
    http_server = HTTPServer(app)
    http_server.bind(4399)
    http_server.start()
    

if __name__ == '__main__':
    main()
