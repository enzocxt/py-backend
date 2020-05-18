import socket
import urllib.parse
import _thread
import json

from utils import (
    log,
    error,
)

# from routes.routes_static import route_dict as static_routes
from routes.routes_static import route_static
from routes.routes_todo import route_dict as todo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.api_todo import route_dict as api_todo


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        """
        获取并添加 headers 中的 cookies
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=', 1)
                self.cookies[k] = v

    def add_headers(self, header):
        """
        Accept-Language: zh-CN,zh;q=0.8
        Coolie: height=169; user=gua
        """
        # 清空 headers
        self.headers = {}
        # lines = header.split('\r\n')
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.add_cookies()

    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            if '=' in arg:
                k, v = arg.split('=', 1)
                f[k] = v
        return f

    def json(self):
        """
        把 body 中的 json 格式字符串解析成 dict 或者 list 并返回
        """
        return json.loads(self.body)


def parsed_path(path):
    """
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path, request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query, request.body)
    r = {
        # '/static': static_routes,
        '/static': route_static,
    }
    # 注册外部的路由
    r.update(todo_routes)
    r.update(user_routes)
    r.update(weibo_routes)
    r.update(api_todo)
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1100)
    r = r.decode('utf-8')
    # log('ip and request, {}\n{}'.format(address, r))
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        connection.close()
    path = r.split()[1]
    # 创建一个新的 request 并设置
    request = Request()
    request.method = r.split()[0]
    eles = r.split('\r\n\r\n', 1)
    request.add_headers(eles[0].split('\r\n')[1:])
    # 把 body 放入 request 中
    request.body = eles[1] if len(eles) > 1 else ''
    # 用 response_for_path 函数来得到 path 对应的响应内容
    response = response_for_path(path, request)
    # 把响应发送给客户端
    connection.sendall(response)
    print('完整响应')
    try:
        log('响应\n', response.decode('utf-8').replace('\r\n', '\n'))
    except Exception as e:
        log('异常', e)
        # 处理完请求, 关闭连接
    connection.close()
    print('关闭')


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 监听 接受 读取请求数据 解码成字符串
        s.listen(5)
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            print('连接成功, 使用多线程处理请求', address)
            # 开一个新的线程来处理请求, 第二个参数是传给新函数的参数列表, 必须是 tuple
            # tuple 如果只有一个值 必须带逗号
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 群里问或者看书/搜索 关键字参数
    run(**config)
