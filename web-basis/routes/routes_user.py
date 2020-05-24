import random

from utils import log
from models.message import Message
from models.user import User
from . import (
    random_str,
    template,
    redirect,
    response_with_headers,
)

message_list = []
session = {}


def current_user(request):
    """
    获得当前的用户
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username


def route_login(request):
    headers = {}
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
    '/login': route_login,
    '/register': route_register,
}
