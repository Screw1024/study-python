# coding:utf-8

import time

def application(env,start_response):
    status = "200 OK"
    headers = [
        ("Content-Type","text/plain")
    ]
    # 调用服务器的start_reponse()函数，并将响应内容给服务器
    start_response(status,headers)
    return time.ctime()
