import random
import json


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


# def template(name):
#     path = 'templates/' + name
#     with open(path, 'r', encoding='utf-8') as fin:
#         return fin.read()


def response_with_headers(headers, status_code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def http_response(body, headers=None):
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def json_response(data):
    """
    本函数返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
    # 注意, content-type 现在是 application/json 而不是 text/html
    # 这个不是很要紧, 因为客户端可以忽略这个
    headers = {
        'Content-Type': 'application/json',
    }
    # json.dumps 用于把 list 或者 dict 转化为 json 格式的字符串
    # ensure_ascii=False 可以正确处理中文
    # indent=2 表示格式化缩进
    body = json.dumps(data, ensure_ascii=False, indent=2)
    return http_response(body, headers=headers)


def redirect(url, headers=None):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    if headers is None:
        headers = {
            'Content-Type': 'text/html',
        }
    # 增加 Location 字段并生成 HTTP 响应返回
    headers['Location'] = url
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
