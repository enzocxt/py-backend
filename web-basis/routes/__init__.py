import random


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'qwertyuiopasdfghjklzxcvbnm,./?><[]{}+_)(*&^%$#@!~`1234567890'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as fin:
        return fin.read()


def response_with_headers(headers, status_code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def http_response(body, headers=''):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # [注意] 没有 HTTP body 部分
    r = response_with_headers(headers, status_code=302) + '\r\n'
    return r.encode('utf-8')


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')
