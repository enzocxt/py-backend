from utils import (
    log,
    template,
)
from models.user import User
from models.weibo import (
    Weibo,
    Comment,
)
from . import (
    random_str,
    redirect,
    response_with_headers,
    http_response,
    error,
)
from .routes_index import current_user


def index(request):
    """
    weibo 首页的路由函数
    """
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    user = User.find_by(username=uname)
    if user is None:
        return redirect('/login')
    weibos = Weibo.find_all(user_id=user.id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def new(request):
    uid = current_user(request)
    user = User.find(uid)
    body = template('weibo_new.html')
    return http_response(body)


def edit(request):
    """
    weibo edit 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 weibo 的 id
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    if w is None:
        return error(request)
    # 权限
    if w.user_id != u.id:
        return redirect('/login')
    body = template('weibo_edit.html', weibo=w)
    return http_response(body)


def add(request):
    """
    用于增加新 weibo 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        w = Weibo(form, u.id)
        w.save()
    return redirect('/weibo')


def update(request):
    """
    用于更新 weibo 的路由函数
    """
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        weibo_id = int(request.query.get('id', -1))
        w = Weibo.find(weibo_id)
        w.content = form.get('content', w.content)
        w.save()
    return redirect('/weibo')


def delete(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    if w.user_id != u.id:
        return redirect('/login')
    if w is not None:
        w.delete()
    return redirect('/weibo')


def comment_add(request):
    uname = current_user(request)
    user = User.find_by(username=uname)
    if user is None:
        return redirect('/login')
    form = request.form()
    c = Comment(form)
    c.user_id = user.id
    c.save()
    return redirect('/weibo')


def login_required(route_func):
    def func(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_func(request)
    return func


route_dict = {
    # GET 请求，显示页面
    '/weibo': index,
    '/weibo/new': new,
    '/weibo/edit': edit,
    # POST 请求，处理数据
    '/weibo/add': add,
    '/weibo/update': login_required(update),
    '/weibo/delete': delete,
    '/comment/add': comment_add,
}
