import random

from utils import (
    log,
    template,
)
from models.message import Message
from .session import session
from . import (
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


def route_index(request):
    """
    主页的处理函数，返回主页的响应
    """
    username = current_user(request)
    body = template('index.html', username=username)
    return http_response(body)


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
    print('请求静态文件：', filename)
    with open(path, 'rb') as f:
        # header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        header = b'HTTP/1.1 200 OK\r\n'
        content = header + b'\r\n' + f.read()
        return content


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


route_dict = {
    '/': route_index,
    '/message': route_message,
}
