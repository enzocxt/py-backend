import socket
import urllib.parse

from routes.routes_index import route_static
from routes.routes_todo import route_dict as todo_routes
from routes.routes_index import route_dict
from utils import log


"""
[------- Socket Server 套路 -------]
Request class
    加上 cookies 和 headers 字段
    简单的 cookie 由用户名组成
routes 中包含所有的路由函数
  静态路由 和 其它路由
  redirect 函数
无限循环监听 request
parse request 得到 method, path, query, body
使用 路由函数 返回不同的 response
models 中包含所有的数据类

url 的规范
第一个 ? 之前的是 path
? 之后的是 query
http://c.cc/search?a=b&c=d&e=1
PATH /search
QUERY a=b&c=d&e=1
"""


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
        key=val 这种形式
        height=168; user=tao
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie:', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=', 1)
                self.cookies[k] = v

    def add_headers(self, headers):
        """
        [
            Accept-Language: zh-CN,zh;q=0.8
            Cookie: height=168; user=tao
        ]
        """
        lines = headers
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.cookies = {}
        self.add_cookies()

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # 使用 urllib.parse.unquote 进行转码
        # username=g+u%26a%3F&password=
        # username=g u&a?&password=
        # 应该在解析出数据后再去 unquote
        args = self.body.split('&')
        args = [urllib.parse.unquote(arg) for arg in args]
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parse_path(path):
    """
    message=hello&author=tao
    ==>
    {
        'message': 'hello',
        'author': 'tao',
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


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    # parse_path 将 path 和 query 分离
    path, query = parse_path(path)
    request.path = path
    request.query = query
    log('path and query:', path, query)
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    r.update(todo_routes)
    response = r.get(path, error)
    return response(request)


def run(host='', port=2000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接收 读取请求数据 解码成字符串
            # [注意] 参数 5 的含义不必关心
            s.listen(5)
            connection, address = s.accept()
            # recv 可以接收客户端发送过来的数据
            # 参数是要接收的字节数
            # 返回值是一个 bytes 类型
            r = b''
            while True:
                tmp = connection.recv(1024)
                r += tmp
                if len(tmp) < 1024:
                    break
            # r = connection.recv(1024)
            # bytes 类型调用 decode('utf-8') 来转成一个字符串(str)
            r = r.decode('utf-8')
            log('原始请求：', r)
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里用判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置 request 的 method
            request.method = r.split()[0]
            rs = r.split('\r\n\r\n', 1)
            request.add_headers(rs[0].split('\r\n')[1:])
            # 把 body 放入 request 中
            request.body = rs[1]
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            # 把响应发送给客户端
            connection.sendall(response)
            # 发送完毕后, 关闭本次连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=2000,
    )
    # 使用 关键字参数
    run(**config)
