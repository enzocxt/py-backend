import random

from utils import log
from models.message import Message
from models.user import User
from .session import session
from . import (
    random_str,
    template,
    redirect,
    response_with_headers,
    http_response,
)

message_list = []


def current_user(request):
    """
    获得当前的用户
    """
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '【游客】')
    return username


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            # server 端 设置 'Set-Cookie' 字段 并发送给 client
            # client 根据 response 中的该字段设置自己 request headers 的 'Cookie' 字段
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # log('headers response:', headers)
            print('登录成功:', user)
            return redirect('/', headers=headers)
        else:
            print('用户名或密码错误')
            return redirect('/login')
    body = template('login.html')
    return http_response(body, headers=headers)


def route_register(request):
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User(form)
        log('注册:', u)
        if u.validate_register():
            u.save()
            # print('注册成功:', u)
            return redirect('/login')
        else:
            return redirect('/register')
    body = template('register.html')
    return http_response(body)


route_dict = {
    '/login': route_login,
    '/register': route_register,
}
