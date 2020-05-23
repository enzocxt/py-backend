import socket
import urllib.parse

from routes import route_static
from routes import route_dict
from utils import log


# [------- Socket Server 套路 -------]
# Request class
# routes 中包含所有的路由函数
#   静态路由 和 其它路由
# 无限循环监听 request
# parse request 得到 method, path, query, body
# 使用 路由函数 返回不同的 response
# models 中包含所有的数据类


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        # username=g+u%26a%3F&password=
        # username=g u&a?&password=
        # TODO, 这实际上算是一个 bug，应该在解析出数据后再去 unquote
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def page(filename):
    with open(filename, encoding='utf-8') as fin:
        return fin.read()


def route_msg():
    """
    msg 页面的处理函数
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image(filename=''):
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    filename = 'doge.gif'
    with open(filename, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


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
            r = connection.recv(1024)
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
            # 把 body 放入 request 中
            request.body = r.split('\r\n\r\n', 1)[1]
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
