# coding:utf-8
import time

# from test_server import HTTPServer

HTML_ROOT_DIR = "./html"

class Application(object):
    """定义一个自己的框架结构"""
    def __init__(self,urls):
        self.urls = urls
    
    # __call__魔法方法，调用时执行
    def __call__(self,env,start_response): 
        # 字典采用.get()和[]索引是一样的，但是如果没有[]会报错
        # ,后面的是默认值
        path = env.get("PATH_INFO","/")

        # /static/index.html，此例的静态文件
        if path.startswith("/static"):
            file_name = path[7:]
              # 读取文件内容，b代表以二进制的方式
            try:
                file = open(HTML_ROOT_DIR + file_name,"rb")
            except IOError:
                # 未找到路由信息，返回404
                status = "404 Not Found"
                headers = []
                start_response(status,headers)
                return "Not Found"
            else:
                file_data = file.read()
                file.close()


                status = "200 OK"
                headers = []
                start_response(status,headers)
                return file_data.decode("utf-8")
        
        for url,handler in self.urls:
            if path == url:
                # 找到请求的文件刚好对应相关的，然后进行处理
                return handler(env,start_response)

        # 未找到路由信息，返回404
        status = "404 Not Found"
        headers = []
        start_response(status,headers)
        return "Not Found"


def show_time(evn,start_response):
    status = "200 OK"
    headers = [
        ("Content-Type","text/plain")
    ]
    start_response(status,headers)
    return time.ctime()

def say_hello(evn,start_response):
    status = "200 Ok"
    headers = [
        ("Content-Type","text/plain")
    ]
    start_response(status,headers)
    return "screw1024 is cool"


urls = [
        ("/",show_time),
        ("/ctime",show_time),
        ("/sayhello",say_hello)
    ]
app = Application(urls)




