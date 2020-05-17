
def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Content-Type': 'text/html',
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意：没有 HTTP body 部分
    # 301 永久重定向， 302 临时（普通）重定向
    # 302 状态码的含义，Location 的作用
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode(encoding='utf-8')


def response_with_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def http_response(body, headers=None):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
