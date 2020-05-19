from models.user import User
from models.weibo import Weibo
from models.comment import Comment

from utils import (
    log,
    template,
    redirect,
    response_with_headers,
    http_response,
    error,
)

from .session import session


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    return user_id


# 定义一个函数统一检测是否登录
def login_required(route_function):
    def func(request):
        uid = current_user(request)
        log('登录鉴定, user_id ', uid)
        if uid == -1:
            # 没登录 不让看 重定向到 /login
            return redirect('/login')
        else:
            # 登录了, 正常返回路由函数响应
            return route_function(request)
    return func


def index(request):
    user_id = request.query.get('user_id', -1)
    if user_id == -1:
        user_id = current_user(request)
    user_id = int(user_id)
    user = User.find(user_id)
    if user is None:
        return redirect('/login')
    # 找到 user 发布的所有 weibo
    weibos = Weibo.find_all(user_id=user_id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def new(request):
    uid = current_user(request)
    user = User.find(uid)
    body = template('weibo_new.html')
    return http_response(body)


def add(request):
    uid = current_user(request)
    user = User.find(uid)
    # 创建微博
    form = request.form()
    w = Weibo(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def delete(request):
    uid = current_user(request)
    user = User.find(uid)
    # 删除微博
    weibo_id = request.query.get('id', None)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    w.delete()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def edit(request):
    weibo_id = request.query.get('id', -1)
    if weibo_id is None:
        weibo_id = current_user(request)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    if w is None:
        return error(request)
    # 生成一个 edit 页面
    body = template('weibo_edit.html',
                    weibo=w)
    return http_response(body)


def update(request):
    uid = current_user(request)
    user = User.find_by(id=uid)
    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    if weibo_id == -1:
        weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    if user.id != w.user_id:
        return error(request)
    w.content = content
    w.save()
    # 重定向到用户的主页
    return redirect('/weibo/index?user_id={}'.format(user.id))


def comment_add(request):
    uid = current_user(request)
    user = User.find(uid)
    # 创建评论
    form = request.form()
    w = Comment(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


# 定义一个函数统一检测是否登录
def login_required(route_function):
    def func(request):
        uid = current_user(request)
        log('登录鉴定, user_id ', uid)
        if uid == -1:
            # 没登录 不让看 重定向到 /login
            return redirect('/login')
        else:
            # 登录了, 正常返回路由函数响应
            return route_function(request)
    return func


route_dict = {
    '/weibo/index': index,
    '/weibo/new': login_required(new),
    '/weibo/edit': login_required(edit),
    '/weibo/add': login_required(add),
    '/weibo/update': login_required(update),
    '/weibo/delete': login_required(delete),
    # 评论功能
    '/comment/add': login_required(comment_add),
}
