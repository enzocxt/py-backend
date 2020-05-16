from utils import log
from utils import template
from utils import redirect
from utils import http_response
from models.user import User
import random

session = {}


def random_str():
    """
    生成一个随机字符串
    """
    seed = "qwertyuiopasdfghjklzxcvbnm1234567890"
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def route_login(request):
    """
    登录页面的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
    }
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            # 设置一个随机字符串来当令牌使用
            session_id = random_str()
            session[session_id] = user.id
            headers['Set-Cookie'] = f'user={session_id}'
            # 下面是把用户名存入 cookie 中
            # headers['Set-Cookie'] = 'user={}'.format(u.username)
            # log('headers response', headers)
            # 登录后重定向到 /
            return redirect('/')
        else:
            result = '用户名或者密码错误'
    # 显示登录页面
    body = template('login.html')
    return http_response(body, headers=headers)


def route_register(request):
    """
    注册页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
            return redirect('/login')
        else:
            # 注册失败 定向到注册页面
            result = '用户名或者密码长度必须大于2'
            return redirect('/register')
    # 显示注册页面
    body = template('register.html')
    return http_response(body)


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


# 路由字典
route_dict = {
    '/login': route_login,
    '/register': route_register,
}
