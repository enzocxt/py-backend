import random

from utils import log
from models.message import Message
from models.user import User


message_list = []
session = {}


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


def route_index(request):
    """
    主页的处理函数，返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    过程：
    <img src="/static?file=doge.gif"/>
    GET /static?file=doge.gif
    path, query = response_for_path('/static?file=doge.gif')
    path = '/static'
    query = {
        'file': 'doge.gif',
    }
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def route_message(request):
    username = current_user(request)
    # 如果是未登录的用户，重定向到 '/'
    if username == '【游客】':
        return redirect('/')
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('POST:', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('message.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def response_with_headers(headers, status_code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def current_user(request):
    """
    获得当前的用户
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username


def route_login(request):
    # header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    headers = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # server 端 设置 'Set-Cookie' 字段 并发送给 client
            # client 根据 response 中的该字段设置自己 request headers 的 'Cookie' 字段
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
        log('注册:', u)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/message': route_message,
    '/login': route_login,
    '/register': route_register,
}
