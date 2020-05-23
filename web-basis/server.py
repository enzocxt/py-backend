import socket


# [------- Socket Server 套路 -------]
# 主要逻辑
# 主路由函数，静态文件路由函数，error 路由函数
# 无限循环监听 request，根据 request 使用 路由函数 返回不同的 response


def log(*args, **kwargs):
    """
    用这个 log 替代 print
    """
    print('log', *args, **kwargs)


def route_index():
    """
    主页的处理函数，返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


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


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/msg': route_msg,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
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
            request = connection.recv(1024)
            # bytes 类型调用 decode('utf-8') 来转成一个字符串(str)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里用 try 防止程序崩溃
                path = request.split()[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # 把响应发送给客户端
                connection.sendall(response)
            except Exception as e:
                log('error', e)
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
